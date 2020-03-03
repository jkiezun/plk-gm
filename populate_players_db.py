import json

def add_player(player):
    from fantasy.models import Player, Club
    if not Player.objects.filter(first_name = player['first_name'], last_name = player['last_name']):
            if Club.objects.filter(name=player['current_club']):
                club_name = Club.objects.get(name=player['current_club'])
            else:
                club_name = Club.objects.get(name="1liga")
            Player.objects.create(
                first_name=player['first_name'],
                last_name=player['last_name'],
                Club=club_name,
                number=player['number'],
                position=player['position']
            )
    else:
        print("Player already in the database")

with open('players.json') as f:
    data = json.load(f)
    for d in data['players']:
        add_player(d)
