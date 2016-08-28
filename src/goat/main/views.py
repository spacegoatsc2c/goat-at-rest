from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from main.models import *
from main.serializers import *

# Create your views here.

class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class CharacterListView(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class RaidsListView(viewsets.ReadOnlyModelViewSet):
    queryset = Raid.objects.all()
    serializer_class = RaidsSerializer

class RaidbossListView(viewsets.ReadOnlyModelViewSet):
    # List the 
    queryset = Boss.objects.all()
    serializer_class = BossSerializer

    def list(self, request, raidid):
        bosses = Boss.objects.filter(raid=raidid).order_by('ordering')

        serializer = self.get_serializer(bosses, many=True)
        return Response(serializer.data) 

class BossListView(viewsets.ReadOnlyModelViewSet):
    queryset = Boss.objects.all()
    serializer_class = BossSerializer
