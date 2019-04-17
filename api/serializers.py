from rest_framework import serializers
from api import models

class UserSerializer(serializers.ModelSerializer):
    user_vip = serializers.CharField(source="get_user_type_display")
    sex_info = serializers.CharField(source="get_sex_display")

    class Meta:
        model = models.UserInfo
        fields = ['id',  'user_vip', 'username', 'password', 'sex', 'sex_info', 'age', 'phone', 'mail']


class WordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseWords
        fields = ['word']

class BookRecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RecommendBook
        fields = ['title', 'author', 'publisher', 'isbn', 'summary', 'simage', 'mimage', 'limage',]

class DouBanBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DouBanBook
        fields = ['title', 'rating', 'votes', 'author', 'publisher',  'summary', 'simage', 'mimage', 'limage',]

class WordHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserWordHistory
        fields = ['word']