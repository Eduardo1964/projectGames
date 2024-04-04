import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# from sklearn.metrics.pairwise import cosine_similarity
# import dash
# import dash_table
# import dash_bootstrap_components as dbc
# import dash_html_components as html
# import dash_core_components as dcc
# import dash_extensions as de
# from dash.dependencies import Input, Output, State
from bs4 import BeautifulSoup
from dateutil.parser import parse
import re
import requests
pages = {}
platform = "ps4"


def extract_date_from_string(text):
    # Define a regular expression pattern to match dates
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b'  # Matches Month DD, YYYY format

    # Search for dates in the text using the regular expression
    dates = re.findall(date_pattern, text)

    # Return the found dates
    return dates

for page in range(100):
    page +=1
    data_page = {
        'name': [],
        'rank': [],
        'rate': [],
        'platform': [],
        'r-date': [],
        'score': [],
        'user score': [],
        'developer': [],
        'genre': [],
        'players': [],
        'critics': [],
        'users': []
    }

    # Site inside metacritic listing "Game Releases by Score"
    # url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=' + str(page)
    url = f'https://www.metacritic.com/browse/game/{platform}/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2024&platform=ps4&page={page}'

    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Printing out current page
    print(50 * '=', "In page: ", page)
    soup.find_all('div', {'class': 'c-finderProductCard'})[2].text
    # Loop through all games in current page
    for game in soup.find_all('div', {'class': 'c-finderProductCard'}):
        # Name
        data_page['name'].append(game.text.split('\n')[0].split('. ')[-1])
        data_page['rank'].append(game.text.split('\n')[0].split('. ')[0])
        print(data_page['name'][-1])
        if data_page['name']=='Injustice 2: Legendary Edition':
            print('stop here')

        data_page['platform'].append(platform)
        data_page['r-date'].append(extract_date_from_string(game.text))
        data_page['score'].append(game.text.split('\n')[-1].split(' Metascore')[0].split(' ')[-1])


#         # Release date
#         data_page['r-date'].append(game.select('div.clamp-details span')[2].text)
#
#         # MetaScore (has different classes depending on score)
#         score_list = [
#             game.find('div', class_='metascore_w large game positive'),
#             game.find('div', class_='metascore_w large game mixed'),
#             game.find('div', class_='metascore_w large game negative')
#         ]
#
#         # Filtering not none element in the score_list
#         score = [s.text for s in score_list if s is not None][0]
#
#         data_page['score'].append(score)
#
#         # User Score (has different classes depending on score)
#         score_list = [
#             game.find('div', class_='metascore_w user large game positive'),
#             game.find('div', class_='metascore_w user large game mixed'),
#             game.find('div', class_='metascore_w user large game negative'),
#             game.find('div', class_='metascore_w user large game tbd')
#         ]
#
#         # Filtering not none element in the score_list
#         score = [s.text for s in score_list if s is not None][0]
#
#         data_page['user score'].append(score)
#
#         # Into the game page
#         # Getting the url of the reviews page:
#         url_info = game.find('a', class_='title')['href']
#
#         url_info = 'https://www.metacritic.com' + url_info
#
#         # Getting into the game page:
#         response_info = requests.get(url_info, headers=user_agent)
#
#         soup_info = BeautifulSoup(response_info.text, 'html.parser')
#
#         # Get developer info
#
#         developer = soup_info.find('li', class_='summary_detail developer')
#
#         if developer is not None:
#             developer = developer.find('span', class_='data').text
#
#             developer = developer.replace('\n', '')
#             developer = developer.replace(' ', '')
#
#             data_page['developer'].append(developer)
#         else:
#             data_page['developer'].append('No info')
#
#         # Get genre info (multiple genres are separated by commas in our entry)
#
#         genres = soup_info.find('li', class_='summary_detail product_genre')
#
#         if genres is not None:
#             genres = genres.find_all('span', class_='data')
#             genre = ''
#
#             for item in genres:
#                 if genre:
#                     genre = genre + ',' + item.text
#                 else:
#                     genre = item.text
#
#             data_page['genre'].append(genre)
#         else:
#             data_page['genre'].append('No info')
#
#         # Get number of players
#
#         players = soup_info.find('li', class_='summary_detail product_players')
#
#         if players is not None:
#             players = players.find('span', class_='data').text
#             data_page['players'].append(players)
#         else:
#             data_page['players'].append('No info')
#
#         # Get number of critics
#
#         critics = soup_info.find('div', class_='score_summary metascore_summary')
#
#         if critics is not None:
#             critics = critics.find('div', class_='summary').find('a').find('span').text
#
#             if critics is not None:
#
#                 critics = critics.replace('\n', '')
#                 critics = critics.replace(' ', '')
#
#                 data_page['critics'].append(critics)
#
#             else:
#                 data_page['critics'].append('0')
#         else:
#             data_page['critics'].append('0')
#
#         # get number of users
#
#         users = soup_info.find('div', class_='details side_details')
#
#         if users is not None:
#             users = users.find('div', class_='score_summary')
#
#             if users is not None:
#                 users = users.find('span', class_='count').find('a')
#
#                 if users is not None:
#                     users = users.text
#                     users = re.sub('\ Ratings$', '', users)
#                     data_page['users'].append(users)
#                 else:
#                     data_page['users'].append('0')
#             else:
#                 data_page['users'].append('0')
#         else:
#             data_page['users'].append('0')
#
#     # create a dict entry to store the dataframe for each page
#     pages[str(page)] = pd.DataFrame(data_page)
#
#     # export page data as csv
#     pages[str(page)].to_csv('games_data-page' + str(page) + '.csv', index=False)
#
# # Create a list of all dataframes to concatenate
# frames = []
#
# for k, v in pages.items():
#     frames.append(v)
#
# df_ultimate = pd.concat(frames)
#
# df_ultimate.index = range(len(df_ultimate))
#
# df_ultimate.to_csv('games-data.csv',index=False)
summary_data=pd.DataFrame.from_dict(data_page)

summary_data.to_csv(f'summary_data_{platform}.csv')
