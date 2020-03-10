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
        fields = ['id', 'first_name', 'last_name',
                  'Club', 'number', 'position']

    def create(self, validated_data):
        club_data = self.validated_data['Club']
        #if not Club.objects.filter(name=club_data['name']):
            
        club = Club.objects.get(name = club_data['name'])
        player = Player.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            Club = club,
            number = validated_data['number'],
            position = validated_data['position']
        )
        return player
