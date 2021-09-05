from rest_framework import serializers

from api.models import user, analysis

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['user_idx', 'user_id', 'user_pw']


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = analysis
        fields = ('analysis_idx', 'user_idx', 'url', 'title', 'thumbnail', 'analysis_date', 'channel_name',
                  'video_time', 'topic', 'script', 'wordcloud', 'topword')