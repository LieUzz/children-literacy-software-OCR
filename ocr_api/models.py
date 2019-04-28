from django.db import models
from usr_api.models import UserInfo
from tool.models import Word

class UserWordHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete = models.DO_NOTHING)
    wordinfo = models.OneToOneField(Word, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

class Words(models.Model):
    zi = models.CharField(max_length=16)
    pinyin = models.CharField(max_length=64,default='')
    bihua = models.CharField(max_length=16,default='')
    pianpang = models.CharField(max_length=16,default='')
    yisi1 = models.CharField(max_length=512,default='')
    yisi2 = models.CharField(max_length=512,default='')
    yisi3 = models.CharField(max_length=512,default='')