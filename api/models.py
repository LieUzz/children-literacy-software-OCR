from django.db import models

class UserInfo(models.Model):
    user_type_choices = (
        (0, '普通用户'),
        (1, 'VIP'),
    )
    user_sex_choices = (
        (0, '男生'),
        (1, '女生'),
        (2, '一位不方便透露性别的人')
    )
    user_type = models.IntegerField(choices = user_type_choices,default=0)
    username = models.CharField(max_length = 32,unique = True)
    password = models.CharField(max_length = 64)
    phone = models.CharField(max_length=128, default=0)
    mail = models.CharField(max_length = 256,default='')
    sex = models.IntegerField(choices = user_sex_choices, default=0)
    age = models.IntegerField(max_length = 32,default=0)

class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    token = models.CharField(max_length = 64)

class UserWordsNum(models.Model):
    user = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    wordsnum = models.IntegerField(max_length= 32, default=0)

class BaseWords(models.Model):
    word = models.CharField(max_length=32)

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

class DouBanBook(models.Model):
    bookid = models.IntegerField(max_length=32)
    rating = models.FloatField(max_length=16,default=0)
    votes = models.IntegerField(max_length=16, default=0)
    title = models.CharField(max_length=64,default='')
    author = models.CharField(max_length=64,default='')
    publisher = models.CharField(max_length=64, default='')
    isbn = models.CharField(max_length=64, default='')
    summary = models.CharField(max_length=3840, default='')
    simage = models.CharField(max_length=128, default='')
    mimage = models.CharField(max_length=128, default='')
    limage = models.CharField(max_length=128, default='')

class TimeGap(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    lasttime = models.IntegerField(max_length=16, default=0)
    one = models.IntegerField(max_length=16, default=0)
    two = models.IntegerField(max_length=16, default=0)
    three = models.IntegerField(max_length=16, default=0)
    four = models.IntegerField(max_length=16, default=0)
    five = models.IntegerField(max_length=16, default=0)
    six = models.IntegerField(max_length=16, default=0)
    seven = models.IntegerField(max_length=16, default=0)
    eight = models.IntegerField(max_length=16, default=0)
    nine = models.IntegerField(max_length=16, default=0)
    ten = models.IntegerField(max_length=16, default=0)

class UserWordHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete = models.DO_NOTHING)
    word = models.CharField(max_length = 16)




