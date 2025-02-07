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
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
pages = {}
platform = "ps4"

def extract_date_from_string(text):
    # Define a regular expression pattern to match dates
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b'  # Matches Month DD, YYYY format

    # Search for dates in the text using the regular expression
    dates = re.findall(date_pattern, text)

    # Return the found dates
    return dates


def scrape_reviews(url, headers, max_pages=3):
    reviews = {}

    # for page in range(1, max_pages * 100, 100):  # Metacritic paginates in steps of 100
    full_url = f"{url}"  # Pagination
    print(f"Scraping: {full_url}")
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Use the correct driver for your browser  # Example URL
    driver.get(full_url)

    # Scroll to load more reviews (adjust range if needed)
    for _ in range(10):  # Scroll 10 times (adjust as needed)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # Wait for reviews to load

    # Get page source after scrolling
    html = driver.page_source
    driver.quit()  # Close the browser
    response = BeautifulSoup(html, "html.parser")
    if response.status_code != 200:
        print(f"Error {response.status_code}: Unable to access {full_url}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all review containers
    review_containers = soup.find('script', text=re.compile('window.__NUXT__')).text

    # Regular expression to match everything after "CriticSummary:" and between { and }
    pattern = r"criticScoreSummary:.*?,publicationSlug:"
    # Search for the pattern
    matches = re.findall(pattern, review_containers)

    for match in matches:
        import ast
        pattern = r'(\w+):("(?:\\.|[^"])*"|[-\w.]+)'

        # Find all matches
        review_pairs = re.findall(pattern, match)
        parsed_dict = {}
        for key, value in review_pairs:
        # Convert "null" and boolean values
            if value == "null":
                value = None
            elif value == "true":
                value = True
            elif value == "false":
                value = False
            elif value.isdigit():  # Convert numbers
                value = int(value)
            elif re.match(r'^-?\d+\.\d+$', value):  # Convert float numbers
                value = float(value)
            elif value.startswith('"') and value.endswith('"'):  # Convert strings
                value = ast.literal_eval(value)  # Safely evaluate escaped string

            parsed_dict[key] = value
        reviewer = parsed_dict['publicationName']
        reviews[reviewer] = parsed_dict

    #TODO retrieving expected data as a dictionary to convert to a dataframe
    time.sleep(2)  # Sleep to prevent getting blocked
    reviews = pd.DataFrame.from_dict(reviews)
    return reviews


def html_to_dict(html):
    soup = BeautifulSoup(html, "html.parser")

    def element_to_dict(element):
        """Recursively convert HTML element to dictionary."""
        tag_dict = {
            "name": element.name,
            "attrs": element.attrs,
            "text": element.text.strip() if element.text else "",
            "children": [element_to_dict(child) for child in element.find_all(recursive=False)]
        }
        return tag_dict

    return element_to_dict(soup.html)


def extract_date_from_string(text):
    # Define a regular expression pattern to match dates
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b'  # Matches Month DD, YYYY format

    # Search for dates in the text using the regular expression
    dates = re.findall(date_pattern, text)

    # Return the found dates
    return dates
data_page = {
        'name': [],
        'rank': [],
        # 'rate': [],
        'platform': [],
        'r-date': [],
        'score': [],
       # 'users':   # 'user score': [],
    #         # 'developer': [],
    #         # 'genre': [],
    #         # 'players': [],
    #         # 'critics': [],
    #        []
    }
# for page in range(100):
#     page +=1
#     # Site inside metacritic listing "Game Releases by Score"
#     # url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=' + str(page)
#     url = f'https://www.metacritic.com/browse/game/{platform}/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2024&platform=ps4&page={page}'
#
#     user_agent = {'User-agent': 'Mozilla/5.0'}
#     response = requests.get(url, headers=user_agent)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Printing out current page
#     print(50 * '=', "In page: ", page)
#
#     # Loop through all games in current page
#     for game in soup.find_all('div', {'class': 'c-finderProductCard'}):
#
#         # Name
#         game_name = game.text.split('\n')[0].split('. ')[-1]
#         data_page['name'].append(game_name)
#         data_page['rank'].append(game.text.split('\n')[0].split('. ')[0])
#         data_page['platform'].append(platform)
#         data_page['r-date'].append(extract_date_from_string(game.text))
#         data_page['score'].append(game.text.split('\n')[-1].split(' Metascore')[0].split(' ')[-1])
#
#         name_nospaces =game_name.strip().replace(' ','-').lower()
#         game_url = f'https://www.metacritic.com/game/{name_nospaces}/critic-reviews/?platform=playstation-4'
#
#         user_agent = {'User-agent': 'Mozilla/5.0'}
#         response_game = requests.get(game_url, headers=user_agent)
#         game_data = BeautifulSoup(response_game.text, 'html.parser')
#         soup_game = BeautifulSoup(response_game.text, 'html.parser')
#
#
#         print(data_page)
#         for game in soup_game.find_all('div', {'class': 'tagstack'}):
#             print(game)
#             data_page['r-date'].append(extract_date_from_string(game.text))
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

summary_data = pd.DataFrame.from_dict(data_page)
print(summary_data.head(30))
summary_data.to_csv(f'summary_data_{platform}.csv')
