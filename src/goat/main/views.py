import shutil
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from main.models import *
from main.serializers import *
from main.management.commands.characterupdate import update_character

# Create your views here.

class UserListView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response()

    def list(self, request):
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response()

class CharacterListView(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def create(self, request):
        data = request.data
        print(data)
        
        # TODO: This should be getting the currently-logged-in user, I think?
        
        user = UserProfile.objects.get(id=data['userid'])

        char = Character()
        char.name = data['name']
        char.realm = data['realm']
        char.user = user

        update_character(char)  # saves it too
        

        serializer = CharacterSerializer(char)
        return Response(serializer.data)

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

        if candidates is not None and len(candidates) > 0:
            return candidates[:1]
        else:
            return Boss.objects.none()

class ArticlesListView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (TokenAuthentication,)
    filter_fields = ('id', 'boss__id', 'boss__name', 
                     'character__id', 'character__name')

    def create(self, request):
        if(request.user):
            data = request.data
            print(data)

            # get the user TODO: this should just use the current logged in user!
            author = UserProfile.objects.get(id=request.user.id)

            # get the boss
            boss = None
            if('boss' in data.keys()):
                boss = Boss.objects.get(pk=data['boss']['id'])

            # get the character
            char = None
            if('character' in data.keys()):
                char = Character.objects.get(pk=data['character']['id'])

            tags = None
            if('tags' in data.keys()):
                tags = data['tags']

            text = None
            if('text' in data.keys()):
                text = data['text']

            link = None
            if('link' in data.keys()):
                link = data['link']


            # build the Article
            article = Article(author=author, article_type=data['article_type'],
                              text=text,
                              tags=tags,
                              boss=boss,
                              character=char,
                              link=link
                              )


        article.save()
        return Response({"status": "success or something"})

class CurrentArticlesListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by("-id")[:10]




class ImagesListView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        data = request.data
        print(data)

        temp_path = data['path']
        orig_filename = data['name']

        shutil.copyfile(temp_path, "/home/quasar/test-images/{}".format(orig_filename))

        return Response({"location": "/img/{}".format(orig_filename)})
