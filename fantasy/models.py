from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class FantasyClub(models.Model):
    name = models.CharField(max_length=35)
    budget = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name



class Player(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    fantasy_club = models.ManyToManyField(
        FantasyClub, through="ClubMember", blank=True)
    Club = models.ForeignKey(Club, on_delete=models.CASCADE)
    number = models.IntegerField(default=99)
    POSITIONS = (
        ("PG", "PG"),
        ("SG", "SG"),
        ("SF", "SF"),
        ("PF", "PF"),
        ("C", "C"),
    )
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default="PG")

    def __str__(self):
        return self.first_name + " " + self.last_name


class ClubMember(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    fantasy_club = models.ForeignKey(
        FantasyClub, on_delete=models.CASCADE)
    starting_five = models.BooleanField()
    sixth_man = models.BooleanField()
    bench_player = models.BooleanField()


class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    play_time = models.CharField(max_length=5)
    fantasy_points = models.IntegerField(blank=True)
    fgm = models.IntegerField(default=0)
    fga = models.IntegerField(default=0)
    twoptm = models.IntegerField(default=0)
    twopta = models.IntegerField(default=0)
    threeptm = models.IntegerField(default=0)
    threepta = models.IntegerField(default=0)
    ftm = models.IntegerField(default=0)
    fta = models.IntegerField(default=0)
    offreb = models.IntegerField(default=0)
    defreb = models.IntegerField(default=0)
    reb = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    plusminus = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    match_round = models.IntegerField()
    opponent = models.ForeignKey(Club, on_delete=models.CASCADE)

    def get_fantasy_points(self):
        score = float(self.points) + float(self.defreb) + float(self.offreb*1.25) + float(self.assists*1.5) + float(
            self.steals*1.5) - float(self.turnovers*1.5) + float(self.blocks*1.5) - float((self.fga - self.fgm)) - float(self.fouls)
        return score

    def save(self, *args, **kwargs):
        self.fantasy_points = self.get_fantasy_points()
        super(PlayerStat, self).save(*args, **kwargs)


class Game(models.Model):
    game_id = models.CharField(max_length=7)

    def __str__(self):
        return self.game_id


class GameRound(models.Model):
    start = models.DateField()
    end = models.DateField()
