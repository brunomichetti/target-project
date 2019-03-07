from django.db import transaction

from targets.models import Target, Match


def targets_match(t1, t2):
    return (t1.topic == t2.topic and
            t1.position.distance(t2.position) <=
            (t1.radius_in_m + t2.radius_in_m))


@transaction.atomic
def generate_matches(sender, instance, created, **kwargs):
    if not created:
        return None
    not_user_targets = Target.objects.exclude(user=instance.user)
    for current_t in not_user_targets:
        if targets_match(instance, current_t):
            new_match = Match(
                target_1=instance,
                target_2=current_t,
                topic=instance.topic
            )
            new_match.save()
