from django.db import models

class user(models.Model):
    # user idx는 자동 생성
    user_id = models.TextField(max_length=100)
    user_pw = models.TextField(max_length=15)

class analysis(models.Model):
    # analysis idx는 자동 생성
    user_idx = models.ForeignKey("user", related_name="user", on_delete=models.CASCADE, db_column="user_idx", default=1)
    url = models.TextField(max_length=300)
    #published = models.CharField(max_length=100)
    title = models.TextField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    analysis_date = models.DateField(auto_now=True)
    channel_name = models.CharField(max_length=100)
    video_time = models.CharField(max_length=20)
    topic = models.TextField(max_length=300)