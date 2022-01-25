import random

from django.db.models.aggregates import Count
from django.db import models


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
