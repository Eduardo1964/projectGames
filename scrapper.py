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


def scrape_reviews(url, game):
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

    text = response.text

    # Regular expression to extract reviews
    pattern = re.findall(r"(\d+)\s+([\w\s]+?)\n\s+(\w+ \d{1,2}, \d{4})\n\s+(.+?)(?:FULL REVIEW)", text, re.DOTALL)

    # Create a list of dictionaries
    data = []
    for match in pattern:
        score, publication, date, review = match
        data.append({
            "Score": int(score),
            "Publication": publication.strip(),
            "Date": date.strip(),
            "Review": review.strip(),
            "Platform": "PlayStation 4"  # Assuming all reviews are for PlayStation 4
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df['Score'] = [int(v.split('\n')[0]) if v[:2].isdigit() else None for v in df['Publication']]
    df['Publication'] = [v.split('\n')[-1].strip() for v in df['Publication']]

    return df


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


summary_data = pd.DataFrame.from_dict(data_page)
print(summary_data.head(30))
summary_data.to_csv(f'summary_data_{platform}.csv')
