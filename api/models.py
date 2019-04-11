from django.db import models

class UserInfo(models.Model):
    user_type_choices = (
        (0, '普通用户'),
        (1, 'VIP'),
    )
    user_type = models.IntegerField(choices = user_type_choices,default=0)
    username = models.CharField(max_length = 32,unique = True)
    password = models.CharField(max_length = 64)
    phone = models.CharField(max_length=128, default=0)
    mail = models.CharField(max_length = 256,default='')
    sex = models.CharField(max_length = 32,default='')
    age = models.CharField(max_length = 32,default='')

class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    token = models.CharField(max_length = 64)

class UserWordsNum(models.Model):
    user = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    wordsnum = models.IntegerField(max_length= 32, default=0)

class BaseWords(models.Model):
    word = models.CharField(max_length=32)

class RecommendBook(models.Model):
    bookname = models.CharField(max_length = 64)
    author = models.CharField(max_length= 64)
    press = models.CharField(max_length= 64, default='')
    isbn = models.CharField(max_length= 64, default='')
    recommendrank = models.IntegerField(max_length=16, default=0)


