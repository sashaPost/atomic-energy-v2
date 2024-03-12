import calendar
import re
import time
import requests
from urllib import response
from bs4 import BeautifulSoup
from django.http import HttpResponse
import os
import threading
import random

from .models import NewsList, Novelty



# new:
source_page_url_ua_2023 = 'https://www.energoatom.com.ua/news-links.html'
source_page_url_ua_2022 = 'https://www.energoatom.com.ua/news-links-2022.html'
source_page_url_en_2023 = 'https://www.energoatom.com.ua/app-eng/news-links.html'
source_page_url_en_2022 = 'https://www.energoatom.com.ua/app-eng/news-links-2022-eng.html'

# old:
source_page_url = 'https://www.energoatom.com.ua/news-links.html'
source_page_2022 = 'https://www.energoatom.com.ua/news-links-2022.html'

file_path = 'scrappy_test/pages/news_list.html'
download_dir = 'scrappy_test/pages/downloaded/'
# not sure if I'm going to use this:
# pages_dir = 'scrappy_test/pages/'
# parsed_dir = 'scrappy_test/pages/parsed/'

# hope not going to use this as well:
# raw_month_names = list(calendar.month_name)
# month_names = [item.lower() for item in raw_month_names[1::]]

def extract_dates(list_of_urls):
    """
    extracts the dates in valid format from the list of novelty URLs.
    """
    valid_dates = []
    pattern = r"\d{6}"
    for url in list_of_urls:
        match = re.search(pattern, url)
        date = match.group()
        year = date[-2:]
        month = date[2:4]
        day = date[:2]
        valid_dates.append(f"{year}-{month}-{day}")
    return valid_dates

def parse_newslist():
    """
    extracts the data about Novelties from the NewsList HTML pages,
    creates Novelty records in the database, marks NewsLists as parsed
    """
    newslist_record = NewsList.objects.filter(parsed=False).first()
    if newslist_record:
        with open(file=newslist_record.file_path, mode='r') as file:
            html = file.read()
        
        soup = BeautifulSoup(markup=html, features='html.parser')
        a_elements = soup.find_all(name='a', class_='theses-item-link')
        hrefs = [ a.get('href') for a in a_elements ]
        list_of_dates = extract_dates(list_of_urls=hrefs)
        
        for novelty_url, date in zip(hrefs, list_of_dates):
            novelty = Novelty.objects.get_or_create(novelty_url=novelty_url, news_list_id=newslist_record, publication_date=date)
            # print(f"{novelty} record created.")
            print("Record created.")
        
        newslist_record.parsed = True
        newslist_record.save() 
        return f"{newslist_record.source_url} parsed."
    return "There's no records left."

def trigger_parse_newslist():
    """
    triggers the parsing of news lists.
    """
    newslist_objects = NewsList.objects.filter(parsed=False)
    while newslist_objects:
        parse_newslist()
    return "Nothing left to parse."

# no longer in use:
# def fill_the_newslist_source_url_ua():
#     """
#     fills the database with the source links (news lists).
#     (run from the shell)
#     """
#     sources_2023 = [ (source_page_url + '#' + month) for month in month_names ]
#     sources_2023.insert(0, source_page_url)
#     for link in sources_2023:
#         NewsList.objects.get_or_create(source_url=link)
    
#     sources_2022 = [ (source_page_2022 + '#' + month) for month in month_names ]
#     sources_2022.insert(0, source_page_2022)
#     for link in sources_2022:
#         NewsList.objects.get_or_create(source_url=link)
#     urls = [ record.source_url for record in NewsList.objects.all() ]
#     return urls

def download_newslist_html_ua():
    """
    Function allows to download the HTML-page by it's 'source_url'
    """
    db_record = NewsList.objects.filter(downloaded_ua=False).first()
    url = db_record.source_url
    filename = url.split('/')[-1]
    
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(download_dir, filename)
        
        with open(file_path, 'w') as file:
            file.write(response.text)
            
        db_record.downloaded_ua = True
        db_record.file_path = file_path
        db_record.save()
        
        print(f'Webpage downloaded and saved.\n{db_record.file_path}')
    else: 
        print('Failed to download webpage.')
    
def trigger_download_ua():
    """
    asynchronously triggers 'download_newslist_html_ua()' allowing to download list of HTML pages 
    using previously generated pages URLs in database
    """
    newslist_objects = NewsList.objects.filter(downloaded_ua=False)
    if newslist_objects:
        delay = random.randint(13, 39)
        time.sleep(delay)
        print(download_newslist_html_ua())
        return trigger_download_ua()
    return 'Nothing left to download.'



# functions above will not work properly 'cause of model fields fixtures
def fill_the_newslist_source_url_eng():
    newslists = NewsList.objects.all()
    
    for nl in newslists:
        ua_url_split = nl.source_url_ua.split(sep='/')
        ua_url_split[1] = ''
        ua_url_split.insert(3, 'app-eng')
        eng_url = ua_url_split
        # print(eng_url)    # check
           
        if '2022' in eng_url[-1]:
            broken_item = eng_url[-1].split(sep='.')
            broken_item[0] += '-eng'
            # print(broken_item)
            eng_url[-1] = broken_item[0] + '.' + broken_item[1]
            # print(eng_url[-1])
        # eng_url.insert(3, '/')
        # eng_url.insert(5, '/')
        sep = '/'
        res_url = sep.join(eng_url)
        # print(res_url)        
        nl.source_url_eng = res_url
        nl.save()

    return "Bye"
