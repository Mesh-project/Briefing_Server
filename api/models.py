
from django.db import models


class model_user(models.Model):
    # user idx는 자동 생성
    user_id = models.TextField(max_length=100)
    user_pw = models.TextField(max_length=15)

class model_analysis(models.Model):
    # analysis idx는 자동 생성
    user_idx = models.ForeignKey("model_user", related_name="model_user", on_delete=models.CASCADE, db_column="user_idx")
    url = models.TextField(max_length=300)
    title = models.TextField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    analysis_date = models.DateField(auto_now=True)
    channel_name = models.CharField(max_length=100)
    video_time = models.CharField(max_length=20)
    video_date = models.CharField(max_length=20)
    topic = models.TextField(max_length=300)
    graph_language = models.CharField(max_length=20)
    graph_bad_comment = models.CharField(max_length=20)