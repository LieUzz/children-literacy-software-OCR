from django.db import models

# Create your models here.

class KidsBook(models.Model):
    isbn = models.CharField(max_length = 24)

