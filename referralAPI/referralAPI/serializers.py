from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    timestamp = serializers.CharField(source='registered_time')

    class Meta:
        model = User
        fields = ["userID", "name", "email", "referral_score", "timestamp"]
