from rest_framework import serializers
from . import models


class WordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseWords
        fields = ['word']