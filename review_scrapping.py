import requests
from bs4 import BeautifulSoup
import time
from scrapper import extract_date_from_string, scrape_reviews
pages = {}
platform = "ps4"
# Set the headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


# Example Metacritic game URL (change based on the game)
GAME_URL = "https://www.metacritic.com/game/pc/elden-ring/user-reviews/"# Example Metacritic game URL (change based on the game)

data_page = {}

for page in range(100):
    page += 1
    # Site inside metacritic listing "Game Releases by Score"
    # url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=' + str(page)
    url = f'https://www.metacritic.com/browse/game/{platform}/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2024&platform=ps4&page={page}'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    for game in soup.find_all('div', {'class': 'c-finderProductCard'}):
        game_info = {}
        # Name
        game_name = game.text.split('\n')[0].split('. ')[-1]
        name_nospaces =game_name.strip().replace(' ','-').lower()
        game_url = f'https://www.metacritic.com/game/{name_nospaces}/critic-reviews/?platform=playstation-4'
        # Printing out current page
        print(50 * '=', "In page: ", page)
        # Scrape reviews
        reviews = scrape_reviews(game_url, headers=HEADERS, max_pages=10)

        data_page[game] = reviews
# Print first 5 reviews
for review in reviews[:5]:
    print(review)
