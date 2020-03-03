import requests
from bs4 import BeautifulSoup
import re
from fantasy.add_stats import add_stats_by_game_id

def update_all_stats():
    schedule_page = requests.get('https://plk.pl/terminarz-i-wyniki.html')
    schedule_page = schedule_page.text
    schedule_page_soup = BeautifulSoup(schedule_page)
    #print(schedule_page)
    games_link = schedule_page_soup.select("td.wynik > a")

    added_rows = 0
    for game in games_link:
        print(game.text.strip())
        print(game['href'])
        game_id = re.findall('\d+', game['href'])[0]
        print(game_id)
        if game.text.strip() != "--:--":
            print(1)
            added_rows = add_stats_by_game_id(game_id)

    return added_rows

update_all_stats()