from main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username')


class CharacterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Character
        depth = 1


class RaidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid

class BossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boss
