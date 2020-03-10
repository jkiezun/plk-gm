from rest_framework import serializers
from fantasy.models import Player, Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name']

class PlayerSerializer(serializers.ModelSerializer):
    Club = ClubSerializer()

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'Club', 'number', 'position']

