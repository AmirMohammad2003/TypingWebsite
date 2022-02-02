"""api.serializers
serializers for the rest api.
"""

from rest_framework import serializers

from .models import UserTest


class RecordSerializer(serializers.ModelSerializer):
    """
    recordSerializer
    serializer for the UserTest model.
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        meta for the recordSerializer.
        """
        model = UserTest
        fields = ('time', 'cpm', 'accuracy', 'quote_id', 'date')
