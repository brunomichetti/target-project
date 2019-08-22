from django.db import transaction
from django.utils.translation import gettext as _
import onesignal as onesignal_sdk

from target.settings import ONE_SIGNAL_AUTH_KEY, ONE_SIGNAL_APP_ID
from targets.models import Target, Match
from users.models import CustomUser

onesignal_client = onesignal_sdk.Client(app_auth_key=ONE_SIGNAL_AUTH_KEY, app_id=ONE_SIGNAL_APP_ID)


def targets_match(t1, t2):
    return (t1.topic == t2.topic and
            t1.position.distance(t2.position) <=
            (t1.radius_in_m + t2.radius_in_m))


def send_match_notification_to_users(user_target, notify_users):
    header = _('New Match!')
    msg = _('Congrats! You have a match with user ' f'{user_target.name}!')
    new_notification = onesignal_sdk.Notification({"en": msg})
    new_notification.set_parameter("headings", {"en": header})
    new_notification.set_parameter("include_player_ids", notify_users)
    onesignal_client.send_notification(new_notification)


def send_msg_notification_to_users(sender_name, to_user_id, message, sent_at):
    header = _('New message from ' f'{sender_name}' '!')
    message = 'Sent at ' + sent_at.strftime('%d-%m-%Y %H:%M') + ': ' + message
    msg = _(message)
    user_notify_id = CustomUser.objects.get(pk=to_user_id).id_notifications
    new_notification = onesignal_sdk.Notification({"en": msg})
    new_notification.set_parameter("headings", {"en": header})
    new_notification.set_parameter("include_player_ids", [user_notify_id])
    onesignal_client.send_notification(new_notification)


@transaction.atomic
def generate_matches(sender, instance, created, **kwargs):
    if not created:
        return None
    not_user_targets = Target.objects.exclude(user=instance.user)
    notify_users = []
    for current_t in not_user_targets:
        if targets_match(instance, current_t):
            new_match = Match(
                target_1=instance,
                target_2=current_t,
                topic=instance.topic
            )
            new_match.save()
            current_usr = CustomUser.objects.filter(id=current_t.user.id).get()
            if not(current_usr.id_notifications in notify_users):
                notify_users.append(current_usr.id_notifications)
    if notify_users != []:
        send_match_notification_to_users(instance.user, notify_users)
