from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File
from .models import ClientUserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'uploaded_at')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class ClientUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUserProfile
        fields = ('email_verified',)