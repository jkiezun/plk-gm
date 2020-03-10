from rest_framework import serializers
from fantasy.models import Player, Club, FantasyClub, ClubMember


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["name"]


class PlayerSerializer(serializers.ModelSerializer):
    Club = ClubSerializer()

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name", "Club", "number", "position"]

    def create(self, validated_data):
        club_data = self.validated_data["Club"]
        # if not Club.objects.filter(name=club_data['name']):

        club = Club.objects.get(name=club_data["name"])
        player = Player.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            Club=club,
            number=validated_data["number"],
            position=validated_data["position"],
        )
        return player


class ClubMemberSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = ClubMember
        fields = ["player", "starting_five", "sixth_man", "bench_player"]


class PlayerStatSerializer(serializers.ModelSerializer):
    players = ClubMemberSerializer(many=True)

    class Meta:
        model = FantasyClub
        fields = [
            "players",
            "play_time",
            "fantasy_points",
            "fgm",
            "fga",
            "twoptm",
            "twopta",
            "threeptm",
            "threepta",
            "ftm",
            "fta",
            "offreb",
            "defreb",
            "reb",
            "assists",
            "turnovers",
            "steals",
            "blocks",
            "fouls",
            "plusminus",
            "points",
            "match_round",
            "opponent",
        ]


class FantasyClubSerializer(serializers.ModelSerializer):
    club_members = ClubMemberSerializer(many=True)

    class Meta:
        model = FantasyClub
        fields = ["name", "budget", "owner", "club_members"]
