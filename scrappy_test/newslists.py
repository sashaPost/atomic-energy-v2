# EXECUTE THE SCRIPT WITH 'python manage.py shell' to avoid import conflicts.
# Get the root directory of your Django project (where manage.py is located)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
SETTINGS_MODULE = 'atomic_energy.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)

# Now you can safely import your Django settings
import django
django.setup()

from django.contrib.auth.models import User
from django.db.models import Q

from bs4 import BeautifulSoup, Comment
import calendar
import random
import requests
from requests.exceptions import RequestException
import re
import time
from datetime import datetime

from scrappy_test.models import NewsList, Novelty




base_url = 'https://www.energoatom.com.ua'
photo_base_uri = 'https://www.energoatom.com.ua/images/dist/bg-photo/'
pdf_base_uri = 'https://www.energoatom.com.ua/parts/pdf-file/'

newslist_url_ua = 'https://www.energoatom.com.ua/news-links.html'    # 2023
newslist_url_old_ua = 'https://www.energoatom.com.ua/news-links-2022.html'
newslist_url_eng = 'https://www.energoatom.com.ua/app-eng/news-links.html'    # 2023
newslist_url_old_eng = 'https://www.energoatom.com.ua/app-eng/news-links-2022-eng.html'

path_ua = 'scrappy_test/pages/downloaded/ua/'
path_en = 'scrappy_test/pages/downloaded/en/'

raw_month_names = list(calendar.month_name)
month_names = [item.lower() for item in raw_month_names[1::]]



def init_delay():
    delay = random.randint(13, 39)
    time.sleep(delay)
    return f'Delay: {delay}s'

def get_novelty_id(novelty_url):
    """
    Accepts and returns string.
    """
    pattern = r"\d{6,8}"
    matches = re.findall(pattern=pattern, string=novelty_url)
    return matches[0]  

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

def create_dirs_if_not(path_ua, path_en):
    """
    Creates directories for HTML files if they don't already exist.
    """
    if not os.path.exists(path_ua) or not os.path.exists(path_en):
        os.makedirs(name=path_ua, exist_ok=True)
        os.makedirs(name=path_en, exist_ok=True)
        return 'Directories created.'
    else:
        return 'Directories already exist.'
    
def download_newslist_html(dir, url):
    """
    Downloads newslist HTML file, rewrites existing (if persisted)
    """
    # print(init_delay())
    try:
        filename = url.split('/')[-1]
        response = requests.get(url)     
        if response.status_code == 200:   
            file_path = os.path.join(dir, filename)
            with open(file_path, 'w') as file:
                file.write(response.text)
            return file_path
    except RequestException as e:
        return f'Error occurred during the download: {str(e)}'
    
def update_nl_db_record(nl_instance, ukr_link, eng_link):
                nl_instance.parsed_ua = 0
                nl_instance.source_url_ua = ukr_link
                nl_instance.file_path_ua = download_newslist_html(path_ua, ukr_link)
                if nl_instance.file_path_ua:
                    nl_instance.downloaded_ua = 1
                    print(f'NewsList record ID {nl_instance.id}\n{nl_instance.source_url_ua}\nwas successfully updated!')
                else:
                    print(f'Couldn\'t download {nl_instance.source_url_ua}')
                
                nl_instance.parsed_eng = 0
                nl_instance.source_url_eng = eng_link
                nl_instance.file_path_eng = download_newslist_html(path_en, eng_link)
                if nl_instance.file_path_eng:
                    nl_instance.downloaded_eng = 1
                    print(f'NewsList record ID {nl_instance.id}\n{nl_instance.source_url_eng}\nwas successfully updated!')
                else:
                    print(f'Couldn\'t download {nl_instance.source_url_eng}')                
                
                return f'NewsList records were successfully updated.'
            
# no longer in use:
# # 'NewsList' manipulations:
# def source_urls_create():
#     """
#     fills the database with the source links (news lists).
#     (run from the shell)
#     """
#     # creates the source links for the news lists (all years and months, including 'eng')
#     sources_ua_2023 = [ (newslist_url_ua + '#' + month) for month in month_names ]
#     sources_ua_2023.insert(0, newslist_url_ua)
#     sources_eng_2023 = [ (newslist_url_eng + '#' + month) for month in month_names ]
#     sources_eng_2023.insert(0, newslist_url_eng)
#     old_sources_ua = [ (newslist_url_old_ua + '#' + month) for month in month_names ]
#     old_sources_ua.insert(0, newslist_url_old_ua)
#     old_sources_eng = [ (newslist_url_old_eng + '#' + month) for month in month_names ]
#     old_sources_eng.insert(0, newslist_url_old_eng)
    
#     source_links_ua = sources_ua_2023 + old_sources_ua
#     source_links_eng = sources_eng_2023 + old_sources_eng
    
#     for ukr_link, eng_link in zip(source_links_ua, source_links_eng):
#         newslist = NewsList.objects.get_or_create(source_url_ua=ukr_link, source_url_eng=eng_link)
#         print(f'News list {newslist[0].id} created')
    
#     return 'Done'
        



base_newslist_urls_ua = [newslist_url_ua, newslist_url_old_ua]
base_newslist_urls_eng = [newslist_url_eng, newslist_url_old_eng]

# This function updates (or creates) 'NewsLists' records along with their corresponding values:
def update_or_create_newslists():
    """
    triggers functions to:
        - create source URLs and put them into the database
        - refresh the newslists (checks if they're already persisted, rewrites them);
        - updates their statuses ('downloaded_ua', 'downloaded_eng'), 'file_path', and the 'updated' timestamp;
    """ 
    
    # 1. Creates directories for HTML files if they don't already exist:
    create_dirs_if_not(path_ua, path_en)
    
    for ukr_link, eng_link in zip(base_newslist_urls_ua, base_newslist_urls_eng):
        # file_path_ua = os.path.join(path_ua, ukr_link.split('/')[-1])
        # file_path_eng = os.path.join(path_en, eng_link.split('/')[-1])
            
        # 2. At this step we're refreshing/creating 'NewsLists' db records with corresponding values,
        # downloading new versions of HTML files:
        db_record = NewsList.objects.get_or_create(source_url_ua=ukr_link)
        if db_record:
            db_newslist = db_record[0]
            
            print(update_nl_db_record(db_newslist, ukr_link, eng_link))
            
            # current_datetime = datetime.now()
            # formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
            # this one is better:
            file_timestamp = datetime.fromtimestamp(os.path.getctime(db_newslist.file_path_ua))
            db_newslist.updated = file_timestamp
            db_newslist.save()
                        
        # else: create 'db_record' refresh file (create a function to rewrite it) 
        else:
            print('SOMETHING WENT WRONG DURING NEWSLISTS UPDATE.')
        
    return 'NewsLists update attempted.'

# commented temporary.
# WORKING ON IT.
def parse_newslist(newslist, file_path):
    with open(file=file_path, mode='r') as file:
        html = file.read()
    
    soup = BeautifulSoup(markup=html, features='html.parser')
    try:
        a_elements = soup.find_all(name='a', class_='theses-item-link')
        if a_elements:
            hrefs = [ a.get('href') for a in a_elements ]
            list_of_dates = extract_dates(list_of_urls=hrefs)   
            for novelty_url, date in zip(hrefs, list_of_dates):
                # print('--------------------------------')
                if 'eng' not in novelty_url:
                    print('UA')          
                    novelty = Novelty.objects.get_or_create(
                        novelty_url_ua=(base_url+novelty_url), 
                        news_list_id=newslist, 
                        parsed_ua=0, 
                        downloaded_ua=0, 
                        publication_date=date,
                    )
                    print(f'Created record for the {novelty[0].novelty_url_ua}')
                else:
                    # print('ENG')
                    novelty_id = re.findall(r'\d{6,}', novelty_url)[0] 
                    try:
                        # novelty = Novelty.objects.filter(novelty_url_ua__contains=novelty_id).first()
                        novelties = Novelty.objects.filter(novelty_url_ua__contains=novelty_id)
                        if novelties:
                            for n in novelties:
                                if ('o-' + novelty_id) in n.novelty_url_ua:
                                    n.novelty_url_eng = base_url+novelty_url
                                    n.parsed_eng=0
                                    n.downloaded_eng=0
                                    n.save()
                        else:
                            print('There\'s nothing matching the query')
                    except AttributeError:
                        novelty = Novelty.objects.get_or_create(
                            novelty_url_eng=(base_url+novelty_url),
                            news_list_id=newslist, 
                            parsed_eng=0, 
                            downloaded_eng=0, 
                            publication_date=date,
                        )
                        if novelty.novelty_url_ua:
                            print(f'Newly created EN Novelty URL:\n{novelty.novelty_url_eng}\nRelated UA Novelty URL:\n{novelty.novelty_url_ua}')
        else:
            return 'Something went wrong collecting "a_elements" in "parse_newslist()"'
    except AttributeError:
        print("Something went wrong in 'parse_newslist()'")
        return AttributeError
    return f'Newslist ID: {newslist.id} was parsed.'

def process_newslists():
    """
    extracts the data about Novelties from the NewsList HTML pages,
    creates Novelty records in the database, marks NewsLists as parsed
    """
    # newslists = NewsList.objects.filter(parsed=False).first()
    newslists = NewsList.objects.filter(Q(parsed_ua=False) | Q(parsed_eng=False))
    
    if newslists:
        for newslist in newslists:    
            # here comes two 'if':
            if newslist.parsed_ua == False:
                print('*****')
                print(f'NewsList ID (UA): {newslist.id}')
                print('*****')
                print(parse_newslist(newslist, newslist.file_path_ua))
                # !!!check if this works on the next run!!!
                newslist.parsed_ua = True
                newslist.save()
                
            if newslist.parsed_eng == False:
                print('*****')
                print(f'NewsList ID (EN): {newslist.id}')
                print('*****')                
                print(parse_newslist(newslist, newslist.file_path_eng))
                # !!!check if this works on the next run!!!
                newslist.parsed_eng = True
                newslist.save()
    return "There's no records left."


        
def init_delay():
    delay = random.randint(13, 39)
    time.sleep(delay)
    return f'Delay: {delay}s'

def download_novelty_html(url, dir):
    filename = url.split('/')[-1]
    response = requests.get(url)     
    if response.status_code == 200:   
        file_path = os.path.join(dir, filename)
        with open(file_path, 'w') as file:
            file.write(response.text)
        return f'{file.name} created successfully.'
    else:
        return 'Something went wrong.'

def trigger_novelty_download():
    lost_ids = []
    novelties = Novelty.objects.all()
    if novelties:
        for novelty in novelties:
            # print(init_delay())
            if (novelty.novelty_url_ua is not False) and (novelty.downloaded_ua == 0):
                ua_url = novelty.novelty_url_ua                 
                try:
                    print(download_novelty_html(url=novelty.novelty_url_ua, dir=path_ua))
                    novelty.downloaded_ua = True
                    novelty.file_path_ua = path_ua + novelty.novelty_url_ua.split('/')[-1]
                    novelty.save()
                    # print(init_delay())
                except RequestException as e:
                    lost_ids.append(novelty.id)
                    print(f'Error occurred during the download: {str(e)}')
            
            if (novelty.novelty_url_eng is not False) and (novelty.downloaded_eng == 0):
                eng_url = novelty.novelty_url_eng
                try:
                    print(download_novelty_html(url=novelty.novelty_url_eng, dir=path_en))
                    novelty.downloaded_eng = True
                    novelty.file_path_eng = path_en + novelty.novelty_url_eng.split('/')[-1]
                    novelty.save()
                    # print(init_delay())
                except RequestException as e:
                    lost_ids.append(novelty.id)
                    print(f'Error occurred during the download: {str(e)}')
    print(lost_ids)
    return 'Nothing left to download.'        



# IT WORKS
# (execute one by one in shell)
# from scrappy_test.newslists import *
# print(update_or_create_newslists())   # uncomment this later
# print(process_newslists())
# print(trigger_novelty_download())