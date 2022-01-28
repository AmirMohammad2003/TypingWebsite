import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Count

UserModel = get_user_model()


class QuoteManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]


class Quote(models.Model):
    content = models.TextField()
    # TODO: length
    # TODO: source
    # TODO: the user who submitted the quote

    objects = models.Manager()
    randoms = QuoteManager()

    def __str__(self):
        if len(self.content) < 60:
            return self.content

        else:
            return self.content[:56] + '...'


class UserStatistics(models.Model):
    tests_started = models.IntegerField(default=0)
    tests_completed = models.IntegerField(default=0)
    time_typing = models.FloatField(default=0)
    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="statistics")

    def __str__(self):
        return f"{self.user.username}'s statistics"


class UserTest(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="tests")
    time = models.FloatField()
    cpm = models.PositiveIntegerField()
    accuracy = models.PositiveIntegerField()
    quote = models.ForeignKey(
        Quote, on_delete=models.SET_NULL, related_name="quote", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quote.content[:50]}..."
