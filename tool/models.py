from django.db import models

# Create your models here.

class KidsBook(models.Model):
    isbn = models.CharField(max_length = 24)

class Word(models.Model):
    word = models.CharField(max_length = 16)
    gif = models.CharField(max_length= 128,default='')
    pinyin = models.CharField(max_length = 128,default='')
    bihua = models.CharField(max_length=16,default='')
    bushou = models.CharField(max_length = 16,default='')
    yisi1 = models.CharField(max_length=640, default='')
    yisi2 = models.CharField(max_length=640, default='')
    yisi3 = models.CharField(max_length=640, default='')
