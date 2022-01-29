"""api.signals
signal registration for api application.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import UserStatistics

user_model = get_user_model()

# I am not happy with this implementation.


@receiver(post_save, sender=user_model)
def create_user_statistics(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    """
    Creates a UserStatistics object for the user.
    """
    if instance.id is not None:
        statistics = UserStatistics.objects.filter(  # pylint: disable=no-member
            user=instance
        )
        if not statistics.exists():
            UserStatistics.objects.create(  # pylint: disable=no-member
                user=instance
            )
