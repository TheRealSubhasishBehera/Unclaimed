from rest_framework import serializers
from .models import User,Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = "__all__"
class AddLostItemSerializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=100)
    item_name = serializers.CharField(max_length=100)
    item_description = serializers.CharField()
    item_location = serializers.CharField()
class PhoneSerializer(serializers.Serializer):
    to_no = serializers.CharField()
    body = serializers.CharField()