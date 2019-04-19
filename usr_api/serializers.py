from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    user_vip = serializers.CharField(source="get_user_type_display")
    sex_info = serializers.CharField(source="get_sex_display")

    class Meta:
        model = models.UserInfo
        fields = ['id',  'user_vip', 'username', 'password', 'sex', 'sex_info', 'age', 'phone', 'mail']