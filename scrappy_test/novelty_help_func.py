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

import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import RequestException
from news.models import *

from django.conf import settings



base_url = 'https://www.energoatom.com.ua'
photo_base_uri = 'https://www.energoatom.com.ua/images/dist/bg-photo/'
pdf_base_uri = 'https://www.energoatom.com/parts/pdf-file/'
tg_video_base_uri = 'https://telegra.ph/file/'

image_dir = 'media/images/'
video_dir = 'media/videos/'
file_dir = 'media/files/'

image_alt = 'Broken image placeholder.'



def get_category():
    category = Category.objects.get_or_create(ua_cat='Попередній сайт', en_cat='Previous Website')[0]
    return category 

# gets and extracts 'title' from 'content_block' to store it in the variable:
def get_exctract_title(content_block):
    try:
        title_tag = content_block.find('h1', class_='single-title')
        if title_tag is not None:
            title_text = title_tag.text
            title_tag.extract()
            content_block
            return title_text
        else:
            return None
    except AttributeError as e:
        print(f'Error appeared during \'title\' extraction: \n{e}')
        return content_block
    
# gets and extracts description ('preview_text_ua') from 'content_block' to store it in the variable:
def get_exctract_description(content_block):
    try:
        description_tag = content_block.find(name='p', class_='single-description')
        if description_tag is not None:
            description_text = description_tag.text
            description_tag.extract()
            return description_text
        else:
            return None
    except AttributeError as e:
        print(f'Error appeared during \'description\' extraction : \n{e}')
        return False

# exludes comments from the content block: 
def extract_comments(content_block):
    try:
        comments = content_block.find_all(string=lambda string: isinstance(string, Comment))
        for comment in comments:
            comment.extract()    
        return content_block
    except AttributeError as e:
        print(f'Error appeared during \'comments\' extraction : \n{e}')
        return content_block
    
def extract_news_links(content_block):
    """
    Extracts news link from the bottom of the content block.
    """
    try:
        news_links = content_block.find('ul', class_='sidebar-body')
        news_links.extract()
        return content_block
    except AttributeError as e:
        print(f'Error appeared during \'news_links\' extraction : \n{e}')
        return content_block
    
def create_download_dirs():
    """
    Creates directories for HTML files if they don't already exist.
    """
    check = (os.path.exists(image_dir) and os.path.exists(file_dir) and os.path.exists(video_dir))
    if not (os.path.exists(image_dir) and os.path.exists(file_dir) and os.path.exists(video_dir)):
        os.makedirs(name=image_dir, exist_ok=True)
        os.makedirs(name=file_dir, exist_ok=True)
        os.makedirs(name=video_dir, exist_ok=True)
        return 'Directories created.'
    else:
        return 'Directories already exist.'
 
def download_image(img_name):    
    create_download_dirs()
    image_url = os.path.join(photo_base_uri, img_name)
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # test:
            # os_abspath = os.path.abspath('.')
            # save_path = os.path.join(MEDIA_ROOT, 'images', img_name)
            save_path = os.path.join(image_dir, img_name)
            with open(save_path, 'wb') as file:
                file.write(response.content)
            # test:
            print(f"Image '{img_name}' downloaded and saved to '{save_path}'")
            return img_name
        else:
            print(f"Failed to download image from '{image_url}', status code: {response.status_code}")
            return False
    except RequestException as e:
        print(f'Error occurred during the download: {str(e)}')
        return False

# fix this one (Make it return something, but 'False'):
def process_preview_image(image_content):
    if image_content['src']:
        img_path = image_content['src']
        img_name = img_path.split('/')[-1]
        down_img_name = download_image(img_name)
        img_parent = image_content.find_parents('div')[2]
        img_parent.extract()
        return down_img_name
    else:
        return False

def unwrap_media(item):
    img = item.find('img')
    yt_video = item.find('iframe')
    if img: 
        wrap = img.find_parents('div')[2]
        wrap.extract()
        return img
    if yt_video:
        wrap = yt_video.find_parents('div')[2]
        wrap.extract()
        return yt_video

# removes the '\n' and CSS attributes from the cotent list:
def remove_n_and_css(cont_list):
    while '\n' in cont_list:
        cont_list.remove('\n')
    for i in range(len(cont_list)):
        if not cont_list[i].find('video'):
            if cont_list[i].has_attr('class'):
                del cont_list[i]['class']
            if cont_list[i].has_attr('id'):
                del cont_list[i]['id']
            for child in cont_list[i].find_all():
                del child['class']
                del child['id']  
    return cont_list

def create_soup(novelty_html):
    try:
        # Reading the UA 'Novelty' HTML file: 
        with open(file=novelty_html, mode='r') as file:
            novelty_html = file.read()
        # initializing 'BeautifulSoup' object:
        soup = BeautifulSoup(novelty_html, 'html.parser')
        # print(soup)
        return soup
    except Exception as e:
        print(e)
        return False

def get_extract_preview_image(clean_content):
    try:
        first_element = clean_content.find_all()[0]
        image_content = first_element.find(name='img', class_='news-img-width')
        if image_content:   
            preview_image_name = process_preview_image(image_content)
            return preview_image_name
    except AttributeError as e:
        print(f'Error appeared during accessing first \'content_block\' element: \n{e}')
        return None

def get_post_using_novelty(novelty):
    try:
        post = novelty.post.first()
        return post
    except Exception as e:
        print(f"'get_post_using_novelty' erro:\n{e}")
        return False

def process_image_with_tag(tag):
    host = settings.ALLOWED_HOSTS[0]
    img_tag = unwrap_media(tag)
    img_url = img_tag['src']
    img_name = img_url.split('/')[-1]
    saved_img_name = download_image(img_name)
    if saved_img_name:
        if host == '127.0.0.1':
            saved_img_path = os.path.join(f'https://{host}:8000/media/images/', saved_img_name)
        else:
            saved_img_path = os.path.join(f'https://{host}/media/images/', saved_img_name)
        img_tag['src'] = saved_img_path
        return {
            'path': saved_img_path,
            'tag': img_tag,
        }
    else:
        return False

