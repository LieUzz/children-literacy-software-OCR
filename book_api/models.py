from django.db import models
from usr_api.models import UserInfo

class RecommendBook(models.Model):
    title = models.CharField(max_length = 64)
    author = models.CharField(max_length= 64)
    publisher = models.CharField(max_length= 64, default='')
    isbn = models.CharField(max_length= 64, default='')
    summary = models.CharField(max_length= 1280, default= '')
    simage = models.CharField(max_length=128, default='')
    mimage = models.CharField(max_length=128, default='')
    limage = models.CharField(max_length=128, default='')
    recommendrank = models.IntegerField(max_length=16, default=0)

class FavoriteBook(models.Model):
    user = models.ForeignKey(UserInfo, on_delete = models.DO_NOTHING)
    isbn = models.CharField(max_length= 64, default='')
    title = models.CharField(max_length=64, default='')
    author = models.CharField(max_length=64,default='')
    publisher = models.CharField(max_length=64, default='')
    isbn = models.CharField(max_length=64, default='')
    summary = models.CharField(max_length=1280, default='')
    simage = models.CharField(max_length=128, default='')
    mimage = models.CharField(max_length=128, default='')
    limage = models.CharField(max_length=128, default='')