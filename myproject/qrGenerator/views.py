from django.shortcuts import render
from qrGenerator.models import User,Item
from qrGenerator.serializers import UserSerializer,ItemSerializer
# Create your views here.
from rest_framework import generics

class Userdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Itemdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ItemSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ItemSerializer