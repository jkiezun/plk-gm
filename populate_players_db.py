import json
from fantasy.models import Player, Club
with open('players.json') as f:
    data = json.load(f)
    for d in data['players']:
        if Club.objects.filter(name=d['current_club']):
            club_name = Club.objects.get(name=d['current_club'])
        else:
            club_name = Club.objects.get(name="1liga")
        Player.objects.create(
            first_name=d['first_name'],
            last_name=d['last_name'],
            Club=club_name,
            number=d['number'],
            position=d['position']
        )
