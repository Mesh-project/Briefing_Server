from django.db import models

# Create your models here.

class user(models.Model):
    user_id = models.TextField(max_length=100)
    user_pw = models.TextField(max_length=15)