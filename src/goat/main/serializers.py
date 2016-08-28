from main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username')

    def create(self, user):
        # never create a user, but return one if it exists
        print(user)
        return UserProfile()


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

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Article
        depth = 1

    def create(self, article):
        print(article)
        #return Article(**article)
        return Article()

