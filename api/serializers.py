from rest_framework import serializers
from api import models

class UserSerializer(serializers.ModelSerializer):
    user_vip = serializers.CharField(source="get_user_type_display")

    class Meta:
        model = models.UserInfo
        fields = ['id',  'user_vip', 'username', 'password', 'phone', 'mail', 'sex', 'age']


class WordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseWords
        fields = ['word']

class BookRecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RecommendBook
        fields = ['bookname', 'author','press', 'isbn', 'recommendrank']
