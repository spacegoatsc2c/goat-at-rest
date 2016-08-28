from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response

from main.models import *
from main.serializers import *

# Create your views here.

class UserListView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class CharacterListView(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class RaidsListView(viewsets.ReadOnlyModelViewSet):
    queryset = Raid.objects.all().order_by('-tier')
    serializer_class = RaidsSerializer

class RaidbossListView(viewsets.ReadOnlyModelViewSet):
    # List the bosses for a given raid
    serializer_class = BossSerializer

    def get_queryset(self):
        raid_id = self.kwargs['raidid']
        return Boss.objects.filter(raid=raid_id).order_by('ordering')


class BossListView(viewsets.ReadOnlyModelViewSet):
    queryset = Boss.objects.all()
    serializer_class = BossSerializer


class CurrentBossListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BossSerializer

    def get_queryset(self):
        # highest level dead boss, highest being based on tier and ordering
        latest_tier = Raid.objects.all().order_by('-tier')[0]
        candidates = Boss.objects.filter(raid=latest_tier, is_dead=True).order_by("-ordering")
        if len(candidates) > 0:
            return candidates[:1]
        else:
            return None

class ArticlesListView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request):
        # {'author': {'username': 'Bob', 'id': 1}, 'article_type': 'text', 'text': 'Hello World'  }
        data = request.data

        # get the user TODO: this should just use the current logged in user!
        author = UserProfile.objects.get(pk=data['author']['id'])

        # get the boss
        boss = Boss.objects.get(pk=data['boss']['id'])

        # get the character
        char = Character.objects.get(pk=data['character']['id'])

        # build the Article
        article = Article(author=author, article_type=data['article_type'],
                          text=data['text'],
                          tags=data['tags'],
                          boss=boss,
                          character=char
                          )


        article.save()
        return Response({"status": "success or something"})

class CurrentArticlesListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by("-id")[:10]
