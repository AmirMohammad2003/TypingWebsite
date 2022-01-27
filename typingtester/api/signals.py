from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import UserStatistics

UserModel = get_user_model()

# I am not happy with this implementation.


@receiver(post_save, sender=UserModel)
def create_user_statistics(sender, instance, created, **kwargs):
    if instance.id is not None:
        statistics = UserStatistics.objects.filter(user=instance)
        if not statistics.exists():
            UserStatistics.objects.create(user=instance)
