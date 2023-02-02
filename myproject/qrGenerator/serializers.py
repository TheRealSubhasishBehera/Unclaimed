from rest_framework import serializers
from .models import User,Item


class ItemSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    items=ItemSerialzer(read_only=True,many=True)
    class Meta:
        model = User
        fields = "__all__"

        