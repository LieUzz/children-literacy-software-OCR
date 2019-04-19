from django.db import models
from usr_api.models import UserInfo

class UserWordHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete = models.DO_NOTHING)
    word = models.CharField(max_length = 16)
    time = models.DateTimeField(auto_now=True)