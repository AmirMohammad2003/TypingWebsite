"""api.models
models for api application.
"""

import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Count

UserModel = get_user_model()


class QuoteManager(models.Manager):  # pylint: disable=too-few-public-methods
    """
    a quote manager to provide getting quotes randomly
    """

    def random(self):
        """returns a random quote"""
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]


class Quote(models.Model):
    """
    Quote model.

    has two fields:
    content: the content of the quote.
    created: the date the quote was created.
    """
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # pylint: disable=fixme
    # TODO: length
    # TODO: source
    # TODO: the user who submitted the quote
    # pylint: enable=fixme

    objects = models.Manager()
    randoms = QuoteManager()

    def __str__(self):
        if len(self.content) < 60:
            return self.content

        return self.content[:56] + '...'  # pylint: disable=unsubscriptable-object


class UserStatistics(models.Model):
    """
    UserStatistics model.
    statistics for a user.
    tests_started: the number of tests started by the user.
    tests_finished: the number of tests finished by the user.
    time_typing: the time the user spent typing.
    user: the user for which the statistics are.
    """
    tests_started = models.IntegerField(default=0)
    tests_completed = models.IntegerField(default=0)
    time_typing = models.FloatField(default=0)
    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="statistics")

    def __str__(self):
        return f"{self.user.username}'s statistics"  # pylint: disable=no-member


class UserTest(models.Model):
    """
    UserTest model.
    a test for a user.
    quote: the quote for the test.
    user: the user for which the test is.
    time: the time the user spent typing.
    cpm: the characters per minute.
    accuracy: the accuracy of the user.
    """
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="tests")
    time = models.FloatField()
    cpm = models.PositiveIntegerField()
    accuracy = models.PositiveIntegerField()
    quote = models.ForeignKey(
        Quote, on_delete=models.SET_NULL, related_name="quote", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quote.content[:50]}..."  # pylint: disable=no-member
