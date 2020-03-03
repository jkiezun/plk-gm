import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from fantasy.models import PlayerStat, Player, Club, Game


def add_stats_by_game_id(game_id):
    if not Game.objects.filter(game_id=game_id):
        res = requests.get("http://www.plk.pl/mecz/" + str(game_id) + "/")

        # using request to proccess polskie znaki
        doc = res.text
        doc = doc.replace("&nbsp", "0")
        for x in range(0, 2):
            df = pd.read_html(doc)[x]

            # drop 1 of 2 rows of headers
            df.columns = df.columns.droplevel(1)

            # renaming headers, because there are duplicates
            df.columns.values[6] = "2fg%"
            df.columns.values[8] = "3fg%"
            df.columns.values[10] = "fg%"
            df.columns.values[12] = 'ft%'

            # dropping insignificant columns
            del df['S5'], df['2fg%'], df['3fg%'], df['fg%'], df['ft%'], df['BO']

            # getting rid of whitespaces in column names
            df.rename(columns={'Czas gry': 'czas_gry', 'Za 2': 'za_2',
                               'Za 3': 'za_3', 'Za 1': 'za_1', 'Z gry': 'z_gry'}, inplace=True)

            # dropping players who Did Not Play
            df = df[df.czas_gry != "DNP"]

            # 2 last columns contain team stats, not significant
            df.drop(df.tail(2).index, inplace=True)

            # split  x/y  columns into separate x and y
            df[['2fgm', '2fga']] = df.za_2.str.split("/", expand=True)
            df[['3fgm', '3fga']] = df.za_3.str.split("/", expand=True)
            df[['ftm', 'fta']] = df.za_1.str.split("/", expand=True)
            df[['fgm', 'fga']] = df.z_gry.str.split("/", expand=True)

            # drop x/y columns
            del df['za_2'], df['za_3'], df['za_1'], df['z_gry']

            # rename to be more human friendly
            df.columns.values[4] = "zb_a"
            df.columns.values[5] = "zb_o"
            df.columns.values[6] = "zb_s"

            # split full name into first and last
            df[['first_name', 'last_name']] = df.Zawodnik.str.split(
                " ", n=1, expand=True)
            del df['Zawodnik']

            # fill None and Nan values with 0's
            df.fillna(value=0, inplace=True)

            # get game round and opponent name
            soup = BeautifulSoup(doc)
            opponents = soup.select('.hedpunc a')
            kolejka = soup.select('.mecz a')[2].getText()
            kolejka = re.findall('\d+', kolejka)[0]
            df['round'] = kolejka
            df['opp'] = opponents[not x].getText()

            # convert numeric columns to numeric type
            cols = list(df.columns)
            cols.remove('first_name')
            cols.remove('last_name')
            cols.remove('czas_gry')
            cols.remove('opp')
            df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

            row_count = 0
            # add stats to database
            for index, row in df.iterrows():
                if Player.objects.filter(first_name=row['first_name'], last_name=row['last_name']):
                    tmp_player = Player.objects.filter(
                        first_name=row['first_name'], last_name=row['last_name'])[0]
                else:
                    tmp_player = Player.objects.create(first_name=row['first_name'], last_name=row['last_name'], Club=Club.objects.get(
                        name=opponents[x].getText()), number=row['NR'], position='SF')
                tmp_opponent = Club.objects.get(name=row['opp'])
                PlayerStat.objects.create(
                    player=tmp_player,
                    play_time=row['czas_gry'],
                    fgm=row['fgm'],
                    fga=row['fga'],
                    twoptm=row['2fgm'],
                    twopta=row['2fga'],
                    threeptm=row['3fgm'],
                    threepta=row['3fga'],
                    ftm=row['ftm'],
                    fta=row['fta'],
                    offreb=row['zb_a'],
                    defreb=row['zb_o'],
                    reb=row['zb_s'],
                    assists=row['A'],
                    turnovers=row['S'],
                    steals=row['P'],
                    blocks=row['B'],
                    fouls=row['F'],
                    plusminus=row['+/-'],
                    points=row['Pkt'],
                    match_round=row['round'],
                    opponent=tmp_opponent
                )
                print(row['last_name'])
                row_count = row_count + 1
        Game.objects.create(game_id=game_id)
        return row_count  # row_count stats added
    else:
        return 0  # game stats already in database, 0 stats added
