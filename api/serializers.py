from rest_framework import serializers

from api.models import user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id','user_id', 'user_pw']