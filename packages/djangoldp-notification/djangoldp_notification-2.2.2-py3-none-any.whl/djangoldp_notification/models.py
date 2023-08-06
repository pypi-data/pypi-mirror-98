import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template import loader
from django.urls import NoReverseMatch, get_resolver
from django.utils.translation import ugettext_lazy as _
from djangoldp.fields import LDPUrlField
from djangoldp.models import Model
from djangoldp.activities.services import ActivityQueueService, ActivityPubService, activity_sending_finished
from djangoldp_notification.middlewares import MODEL_MODIFICATION_USER_FIELD
from djangoldp_notification.permissions import InboxPermissions, SubscriptionsPermissions
from djangoldp_notification.views import LDPNotificationsViewSet
import logging


logger = logging.getLogger('djangoldp')


class Notification(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox', on_delete=models.deletion.CASCADE)
    author = LDPUrlField()
    object = LDPUrlField()
    type = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta(Model.Meta):
        owner_field = 'user'
        ordering = ['-date']
        permission_classes = [InboxPermissions]
        anonymous_perms = ['add']
        authenticated_perms = ['inherit']
        owner_perms = ['view', 'change', 'control']
        view_set = LDPNotificationsViewSet

    def __str__(self):
        return '{}'.format(self.type)

    def save(self, *args, **kwargs):
        # I cannot send a notification to myself
        if self.author.startswith(settings.SITE_URL):
            try:
                # author is a WebID.. convert to local representation
                author = Model.resolve(self.author.replace(settings.SITE_URL, ''))[1]
            except NoReverseMatch:
                author = None
            if author == self.user:
                return

        super(Notification, self).save(*args, **kwargs)

class NotificationSetting(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings")
    receiveMail = models.BooleanField(default=True)

    class Meta:
        auto_author = 'user'
        owner_field = 'user'
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = ['view', 'change']
        container_path = 'settings/'
        serializer_fields = ['@id', 'receiveMail']
        rdf_type = 'sib:usersettings'

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.user.urlid)

class Subscription(Model):
    object = models.URLField()
    inbox = models.URLField()
    field = models.CharField(max_length=255, blank=True, null=True,
                             help_text='if set to a field name on the object model, the field will be passed instead of the object instance')

    def __str__(self):
        return '{}'.format(self.object)

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ["add", "view", "delete"]
        permission_classes = [SubscriptionsPermissions]


@receiver(post_save, sender=Subscription, dispatch_uid="nested_subscriber_check")
def create_nested_subscribers(sender, instance, created, **kwargs):
    # save subscriptions for one-to-many nested fields
    if created and not instance.is_backlink and instance.object.startswith(settings.SITE_URL):
        try:
            # object is a WebID.. convert to local representation
            local = Model.resolve(instance.object.replace(settings.SITE_URL, ''))[0]
            nested_fields = Model.get_meta(local, 'nested_fields', [])

            # Don't create nested subscriptions for user model (Notification loop issue)
            if local._meta.model_name == get_user_model()._meta.model_name:
                return

            for nested_field in nested_fields:
                try:
                    field = local._meta.get_field(nested_field)
                    nested_container = field.related_model
                    nested_container_url = Model.absolute_url(nested_container)

                    if field.one_to_many:
                        # get the nested view set
                        nested_url = str(instance.object) + '1/' + nested_field + '/'
                        view, args, kwargs = get_resolver().resolve(nested_url.replace(settings.SITE_URL, ''))
                        # get the reverse name for the field
                        field_name = view.initkwargs['nested_related_name']

                        if field_name is not None and field_name != '':
                            # check that this nested-field subscription doesn't already exist
                            existing_subscriptions = Subscription.objects.filter(object=nested_container_url, inbox=instance.inbox,
                                                                                 field=field_name)
                            # save a Subscription on this container
                            if not existing_subscriptions.exists():
                                Subscription.objects.create(object=nested_container_url, inbox=instance.inbox, is_backlink=True,
                                                            field=field_name)
                except:
                    pass
        except:
            pass



# --- SUBSCRIPTION SYSTEM ---
@receiver(post_save, dispatch_uid="callback_notif")
@receiver(post_delete, dispatch_uid="delete_callback_notif")
def send_notification(sender, instance, **kwargs):
    if(type(instance).__name__ != "ScheduledActivity" and type(instance).__name__ != "LogEntry" and type(instance).__name__ != "Activity"):
        if sender != Notification:
            # don't send notifications for foreign resources
            if hasattr(instance, 'urlid') and Model.is_external(instance.urlid):
                return

            recipients = []
            try:
                url_container = settings.BASE_URL + Model.container_id(instance)
                url_resource = settings.BASE_URL + Model.resource_id(instance)
            except NoReverseMatch:
                return

            # dispatch a notification for every Subscription on this resource
            for subscription in Subscription.objects.filter(models.Q(object=url_resource) | models.Q(object=url_container)):
                if subscription.inbox not in recipients and (not subscription.is_backlink or not kwargs.get("created")):
                    # I may have configured to send the subscription to a foreign key
                    if subscription.field is not None and len(subscription.field) > 1:
                        try:
                            if kwargs.get("created"):
                                continue

                            instance = getattr(instance, subscription.field, instance)

                            # don't send notifications for foreign resources
                            if hasattr(instance, 'urlid') and Model.is_external(instance.urlid):
                                continue

                            url_resource = settings.BASE_URL + Model.resource_id(instance)
                        except NoReverseMatch:
                            continue
                        except ObjectDoesNotExist:
                            continue

                    send_request(subscription.inbox, url_resource, instance, kwargs.get("created"))
                    recipients.append(subscription.inbox)


@receiver(activity_sending_finished, sender=ActivityQueueService)
def _handle_prosody_response(sender, response, saved_activity, **kwargs):
    '''callback function for handling a response from Prosody on a notification'''
    # if text is defined in the response body then it's an error
    if saved_activity is not None:
        response_body = saved_activity.response_to_json()
        if 'condition' in response_body:
            logger.error("[DjangoLDP-Notification.models._handle_prosody_response] error in Prosody response " +
                         str(response_body))


def send_request(target, object_iri, instance, created):
    author = getattr(getattr(instance, MODEL_MODIFICATION_USER_FIELD, None), "urlid", str(_("Auteur inconnu")))
    if(created is not None):
        request_type = "creation" if created else "update"
    else:
        request_type = "deletion"

    # local inbox
    if target.startswith(settings.SITE_URL):
        user = Model.resolve_parent(target.replace(settings.SITE_URL, ''))
        Notification.objects.create(user=user, object=object_iri, type=request_type, author=author)
    # external inbox
    else:
        json = {
            "@context": settings.LDP_RDF_CONTEXT,
            "object": object_iri,
            "author": author,
            "type": request_type
        }
        ActivityQueueService.send_activity(target, json)


@receiver(post_save, sender=Notification)
def send_email_on_notification(sender, instance, created, **kwargs):
    if created and instance.summary and getattr(settings,'JABBER_DEFAULT_HOST',False) and instance.user.email:
        # get author name, and store in who
        try:
            # local author
            if instance.author.startswith(settings.SITE_URL):
                who = str(Model.resolve_id(instance.author.replace(settings.SITE_URL, '')))
            # external author
            else:
                who = requests.get(instance.author).json()['name']
        except:
            who = "Quelqu'un"

        # get identifier for resource triggering notification, and store in where
        try:
            if instance.object.startswith(settings.SITE_URL):
                where = str(Model.resolve_id(instance.object.replace(settings.SITE_URL, '')))
            else:
                where = requests.get(instance.object).json()['name']
        except:
            where = "le chat"

        if who == where:
            where = "t'a envoyé un message privé"
        else:
            where = "t'a mentionné sur " + where

        on = (getattr(settings, 'INSTANCE_DEFAULT_CLIENT', False) or settings.JABBER_DEFAULT_HOST)

        html_message = loader.render_to_string(
            'email.html',
            {
                'on': on,
                'instance': instance,
                'author': who,
                'object': where
            }
        )

        if instance.user.settings.receiveMail:
            send_mail(
                'Notification sur ' + on,
                instance.summary,
                (getattr(settings, 'EMAIL_HOST_USER', False) or "noreply@" + settings.JABBER_DEFAULT_HOST),
                [instance.user.email],
                fail_silently=True,
                html_message=html_message
            )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_settings(sender, instance, created, **kwargs):
    try:
        if created and instance.urlid.startswith(settings.SITE_URL):
            NotificationSetting.objects.create(user=instance)
    except:
        pass
