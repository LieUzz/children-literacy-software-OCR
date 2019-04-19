from rest_framework import serializers
from . import models

class WordHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserWordHistory
        fields = ['word']