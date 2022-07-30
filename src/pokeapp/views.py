from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .models import Pokemon, Sprite
from .serializers import UserSerializer, PokemonSerializer, SpriteSerializer

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PokemonViewSet(viewsets.ModelViewSet):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.AllowAny]

class SpriteViewSet(viewsets.ModelViewSet):

    queryset = Sprite.objects.all()
    serializer_class = SpriteSerializer
    permission_classes = [permissions.AllowAny]