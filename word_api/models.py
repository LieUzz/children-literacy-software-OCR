from django.db import models
from usr_api.models import UserInfo

class UserWordsNum(models.Model):
    user = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    wordsnum = models.IntegerField(max_length= 32, default=0)

class BaseWords(models.Model):
    word = models.CharField(max_length=32)
