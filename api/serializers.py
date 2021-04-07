from rest_framework import serializers

from api.models import model_user, model_analysis


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = model_user
        fields = ['id','user_id', 'user_pw']

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = model_analysis
        fields = ('id','user_idx', 'url', 'title', 'thumbnail', 'analysis_date', 'channel_name',
                  'video_time', 'video_date', 'topic', 'graph_language', 'graph_bad_comment')