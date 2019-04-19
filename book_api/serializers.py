from rest_framework import serializers
from . import models

class BookRecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RecommendBook
        fields = ['title', 'author', 'publisher', 'isbn', 'summary', 'simage', 'mimage', 'limage']

class FavoriteBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FavoriteBook
        fields = ['title', 'author', 'publisher', 'isbn', 'summary', 'simage', 'mimage', 'limage']