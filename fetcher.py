import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import random
import os
import re
from utils import parse_date
from datetime import datetime, timedelta

def get_useragent():
    return random.choice(_useragent_list)

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]

def fetch_news(start_date, end_date, news_type):

    url = f'https://www.okx.com/ru/help/section/announcements-{news_type}'
    resp = requests.get(url, headers={"User-Agent": get_useragent()})
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    news_items = []

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    page_links = soup.find_all('a', class_='okui-pagination-item okui-pagination-item-link')

    page_numbers = [int(link.text) for link in page_links]

    total_pages = max(page_numbers) if page_numbers else 0

    articles = soup.find_all('a', class_='okui-powerLink index_articleItem__d-8iK')

    for article in articles:
        title = article.find('div', class_='index_title__iTmos index_articleTitle__ys7G7').text.strip()
        date_str = article.find('span', class_='').text.strip()
        date = parse_date(date_str)

        if date < start_date:
            break

        if start_date <= date <= end_date:
            news_items.append({'title': title, 'date': date})

    
    for i in range(2, total_pages+1):
        url2 = f'https://www.okx.com/ru/help/section/announcements-{news_type}/page/{i}'

        try:
            resp = requests.get(url2, headers={"User-Agent": get_useragent()})
            resp.raise_for_status()

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return news_items
            
            else:
                raise 

        soup = BeautifulSoup(resp.text, 'html.parser')
        articles = soup.find_all('a', class_='okui-powerLink index_articleItem__d-8iK')

        if not articles:
            return news_items
        
        for article in articles:
            title = article.find('div', class_='index_title__iTmos index_articleTitle__ys7G7').text.strip()
            date_str = article.find('span', class_='').text.strip()

            date = parse_date(date_str)

            if date < start_date:
                return news_items

            if start_date <= date <= end_date:
                news_items.append({'title': title, 'date': date})

        i += 1
    
    return news_items

def save_to_folder(news_items, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    df = pd.DataFrame(news_items)
    file_path = os.path.join(folder, 'okx_news.csv')
    df.to_csv(file_path, index=False)
