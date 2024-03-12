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
from datetime import datetime

from slugify import slugify
from transliterate import translit

from news.models import *
from scrappy_test.models import *
from scrappy_test.parse_ua_novelty import *
from scrappy_test.parse_en_novelty import *
from scrappy_test.novelty_help_func import *
from django.contrib.auth.models import User

# print(MEDIA_ROOT)

base_url = 'https://www.energoatom.com.ua'
photo_base_uri = 'https://www.energoatom.com.ua/images/dist/bg-photo/'
pdf_base_uri = 'https://www.energoatom.com/parts/pdf-file/'
tg_video_base_uri = 'https://telegra.ph/file/'

image_dir = 'media/images/'
video_dir = 'media/videos/'
file_dir = 'media/files/'

image_alt = 'Broken image placeholder.'



# # gets and extracts 'title' from 'content_block' to store it in the variable:
# def get_exctract_title(content_block):
#     try:
#         title_tag = content_block.find('h1', class_='single-title')
#         title_text = title_tag.text
#         title_tag.extract()
#         content_block
#         return title_text
#     except AttributeError as e:
#         print(f'Error appeared during \'title\' extraction: \n{e}')
#         return content_block
    
# # gets and extracts description ('preview_text_ua') from 'content_block' to store it in the variable:
# def get_exctract_description(content_block):
#     try:
#         description_tag = content_block.find(name='p', class_='single-description')
#         description_text = description_tag.text
#         description_tag.extract()
#         return description_text
#     except AttributeError as e:
#         print(f'Error appeared during \'description\' extraction : \n{e}')
#         return False
 
# # exludes comments from the content block: 
# def extract_comments(content_block):
#     try:
#         comments = content_block.find_all(string=lambda string: isinstance(string, Comment))
#         for comment in comments:
#             comment.extract()    
#         return content_block
#     except AttributeError as e:
#         print(f'Error appeared during \'comments\' extraction : \n{e}')
#         return content_block
    
# def extract_news_links(content_block):
#     """
#     Extracts news link from the bottom of the content block.
#     """
#     try:
#         news_links = content_block.find('ul', class_='sidebar-body')
#         news_links.extract()
#         return content_block
#     except AttributeError as e:
#         print(f'Error appeared during \'news_links\' extraction : \n{e}')
#         return content_block
    
# def create_download_dirs():
#     """
#     Creates directories for HTML files if they don't already exist.
#     """
#     check = (os.path.exists(image_dir) and os.path.exists(file_dir) and os.path.exists(video_dir))
#     if not (os.path.exists(image_dir) and os.path.exists(file_dir) and os.path.exists(video_dir)):
#         os.makedirs(name=image_dir, exist_ok=True)
#         os.makedirs(name=file_dir, exist_ok=True)
#         os.makedirs(name=video_dir, exist_ok=True)
#         return 'Directories created.'
#     else:
#         return 'Directories already exist.'
    
# not being used yet:
# def download_pdf_file(file_name):
#     create_download_dirs()
#     file_url = os.path.join(pdf_base_uri, file_name)
#     try:
#         response = requests.get(file_url)
#         if response.status_code == 200:
#             save_path = os.path.join(os.path.abspath('..'), file_dir, file_name)
#             with open(save_path, 'wb') as file:
#                 file.write(response.content)
#             return save_path
#         else:
#             print(f"Failed to download PDF file from '{file_url}', status code: {response.status_code}")
#             return False
#     except RequestException as e:
#         print(f'Error occurred during the download: {str(e)}')
#         return False
    
# def download_image(img_name):    
#     create_download_dirs()
#     image_url = os.path.join(photo_base_uri, img_name)
#     try:
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             # test:
#             # os_abspath = os.path.abspath('.')
#             # save_path = os.path.join(MEDIA_ROOT, 'images', img_name)
#             save_path = os.path.join(image_dir, img_name)
#             with open(save_path, 'wb') as file:
#                 file.write(response.content)
#             # test:
#             print(f"Image '{img_name}' downloaded and saved to '{save_path}'")
#             return img_name
#         else:
#             print(f"Failed to download image from '{image_url}', status code: {response.status_code}")
#             return False
#     except RequestException as e:
#         print(f'Error occurred during the download: {str(e)}')
#         return False

# def process_preview_image(image_content):
#     if image_content['src']:
#         img_path = image_content['src']
#         img_name = img_path.split('/')[-1]
#         down_img_name = download_image(img_name)
#         img_parent = image_content.find_parents('div')[2]
#         img_parent.extract()
#         return down_img_name
#     else:
#         return False

# def unwrap_media(item):
#     img = item.find('img')
#     yt_video = item.find('iframe')
#     if img: 
#         wrap = img.find_parents('div')[2]
#         wrap.extract()
#         return img
#     if yt_video:
#         wrap = yt_video.find_parents('div')[2]
#         wrap.extract()
#         return yt_video

# # removes the '\n' and CSS attributes from the cotent list:
# def remove_n_and_css(cont_list):
#     while '\n' in cont_list:
#         cont_list.remove('\n')
#     for i in range(len(cont_list)):
#         if not cont_list[i].find('video'):
#             if cont_list[i].has_attr('class'):
#                 del cont_list[i]['class']
#             if cont_list[i].has_attr('id'):
#                 del cont_list[i]['id']
#             for child in cont_list[i].find_all():
#                 del child['class']
#                 del child['id']  
#     return cont_list

# def create_soup(novelty_html):
#     try:
#         # Reading the UA 'Novelty' HTML file: 
#         with open(file=novelty_html, mode='r') as file:
#             novelty_html = file.read()
#         # initializing 'BeautifulSoup' object:
#         soup = BeautifulSoup(novelty_html, 'html.parser')
#         # print(soup)
#         return soup
#     except Exception as e:
#         print(e)
#         return False
    
# def old_posts_category():
#     ua_message = 'Попередній сайт'
#     en_message = 'Previous Website'
#     category = Category.objects.get_or_create(ua_cat=ua_message, en_cat=en_message)
#     return category
    
# def get_extract_preview_image(clean_content):
#     try:
#         first_element = clean_content.find_all()[0]
#         image_content = first_element.find(name='img', class_='news-img-width')
#         if image_content:   
#             preview_image_name = process_preview_image(image_content)
#             return preview_image_name
#     except AttributeError as e:
#         print(f'Error appeared during accessing first \'content_block\' element: \n{e}')
#         return False

# def parse_ua_head(novelty):
#     # has to be passed while creating the Post model instance:
#     admin = User.objects.get(username='admin')
#     # image_alt = 'Broken image placeholder.'
#     novelty_html = novelty.file_path_ua
#     # print(novelty_html)
#     old_date = novelty.publication_date
#     new_date = '20' + old_date
#     formatted_pub_date = datetime.strptime(new_date, '%Y-%m-%d').strftime('%Y-%m-%d')
#     # print(formatted_pub_date)
#     soup = create_soup(novelty_html)
#     # print(soup)
#     content = soup.find('div', class_="col-10 col-sm-8 col-md-10 col-lg-10 col-xl-9 col-xxl-10")
#     # print(content)
#     extracted_comments = extract_comments(content)
#     # print(extracted_comments)
#     clean_content = extract_news_links(extracted_comments)
#     # print(clean_content)
#     title = get_exctract_title(clean_content)
#     if title:
#         title = title.strip()
#     # print(title)
#     description = get_exctract_description(clean_content)
#     if description:
#         description = description.strip()
#     # print(description)
#     preview_image = get_extract_preview_image(clean_content)
#     print(preview_image)
#     preview_image_bd_path = os.path.join('images', preview_image)
#     if not preview_image:
#         preview_image = False
#         preview_image_pd_path = False 
#     # print(preview_image)
#     # !!! should be the 'Category' model instance !!!
#     category = False
#     if not category:
#     #     category = old_posts_category()
#         category = Category.objects.filter(id=1).first()
        
#     # test:
#     # novelty_id = novelty.id
#     # print(novelty_id)
    
#     # !!! fix 'title' and 'description' !!!
#     post = Post.objects.get_or_create(
#         meta_title=title,
#         meta_description=description,
#         preview_image=preview_image_bd_path,
#         image_alt=image_alt,
#         indicated_date=formatted_pub_date,  
#         added_by=admin,
#         migrated_novelty=True,
#         novelty_id=novelty, 
#         old_date=formatted_pub_date,
#         category=category,
#     )
#     # Now it's time to create 'UaPostHead' instance. 
#     transliterated_title = translit(title, 'uk', reversed=True)
#     slug = slugify(transliterated_title, allow_unicode=True)
#     ua_post_head = UaPostHead.objects.get_or_create(
#         post=post[0], 
#         title_ua=title, 
#         slug=slug,
#         preview_text_ua=description
#     )

#     if post and ua_post_head:
#         return {
#             'post': post[0],
#             'ua_post_head': ua_post_head[0],
#             'clean_content': clean_content,
#         }
#     else:
#         False

# def get_post_using_novelty(novelty):
#     try:
#         post = novelty.post.first()
#         return post
#     except Exception as e:
#         print(f"'get_post_using_novelty' erro:\n{e}")
#         return False

# def process_image_with_tag(tag):
#     img_tag = unwrap_media(tag)
#     img_url = img_tag['src']
#     img_name = img_url.split('/')[-1]
#     saved_img_name = download_image(img_name)
#     if saved_img_name:
#         saved_img_path = os.path.join('images/', saved_img_name)
#         img_tag['src'] = saved_img_path
#         return {
#             'path': saved_img_path,
#             'tag': img_tag,
#         }
#     else:
#         return False
    
# def parse_ua_body(content, novelty):
#     """
#     'cleaning' the rest of  content, 
#     creating 'UaPostBody' instances during iteration
#     through 'content list'.
#     """
#     # image_alt = 'Broken image placeholder.'
    
#     cont_list = content.contents
#     cont_list = remove_n_and_css(cont_list)

#     counter = 0
#     content_block = []
#     content_string = ''
    
#     post = get_post_using_novelty(novelty)
    
#     for i in cont_list:
#         # images:
#         if i.find('img'):
#             saved_img = process_image_with_tag(i)
#             if saved_img:
#                 i['src'] = saved_img['path']
#             content_block.append(i)
            
#             for item in content_block:
#                 content_string += str(item) + '\n'
#             # print(content_string)
#             content_block.clear()
            
#             ua_post_body = UaPostBody.objects.get_or_create(
#                 post = post,
#                 message_ua = content_string,
#                 image = saved_img['path'],
#                 post_image_alt = image_alt,
#                 # there's no 'video_url' if 'PostBody' image is being processed:
#                 video_url = False,
#             )            
#             # print(ua_post_body)
#             counter += 1
#             content_string = ''
#         # YouTube:
#         elif i.find('iframe'):
#             yt_video_tag = unwrap_media(i)    
#             yt_video_url = yt_video_tag['src']    # works
#             content_block.append(yt_video_tag)
            
#             for item in content_block:
#                 content_string += str(item) + '\n'
#             content_block.clear()
            
#             image_alt = 'Model instance has no image.'
            
#             ua_post_body = UaPostBody.objects.get_or_create(
#                 post = post,
#                 message_ua = content_string,
#                 image = False,
#                 post_image_alt = image_alt,
#                 video_url = yt_video_url,
#             )           
                
#             counter += 1
#             content_string = ''
#         # TG video:
#         elif i.find('video'):
#             tg_video_tag = i.find('video')
#             tg_video_url = i.find('video')['src']
#             content_block.append(tg_video_tag)

#             for item in content_block:
#                 content_string += str(item) + '\n'
#             content_block.clear()
            
#             image_alt = 'Model instance has no image.'
            
#             ua_post_body = UaPostBody.objects.get_or_create(
#                 post = post,
#                 message_ua = content_string,
#                 image = False,
#                 post_image_alt = image_alt,
#                 video_url = tg_video_url,
#             )           
            
#             counter += 1
#             content_string = ''
            
#         # !!! DO THIS LATER !!!
#         # PDF files:
#         # getting an error trying to download the file
#         # IGNORE FILES FOR NOW:
#         # internal URLs left
#         # ALONG WITH URLs.
#         # elif i.find('a'):
#         #     a_tag = i.find('a')
#         #     url = a_tag['href']
#         #     filename = url.split('/')[-1]
#         #     ext = url.split('.')[-1]
#         #     if ext == 'pdf':
#         #         saved_file_path = download_pdf_file(filename)
#         #         if saved_file_path:        
#         #             a_tag['href'] = saved_file_path 
#         #     content_block.append(a_tag)
#         #     counter += 1
#         #     print(f'Block #: {counter}')
#         #     print(content_block)
#         else:
#             content_block.append(i)
            
#         if content_string == '':
#             image_alt = 'Model instance has no image or video.'
            
#             ua_post_body = UaPostBody.objects.get_or_create(
#                 post = post,
#                 message_ua = content_string,
#                 image = False,
#                 post_image_alt = image_alt,
#                 video_url = False,
#             )     
            
#             counter += 1
#             content_string = ''
            
#     return post.ua_body.all()
          
# def parse_ua(novelty):
#     ua_post_head = parse_ua_head(novelty)
#     post_body_content = ua_post_head['clean_content']
#     ua_post_body = parse_ua_body(post_body_content, novelty)
#     if ua_post_head and ua_post_body:
#         return {
#             'ua_post_head': ua_post_head,
#             'ua_post_body': ua_post_body,
#         }
#     else:
#         return False
    
# # !!!
# def parse_en(novelty):
#     pass

# Execute it in the loop iterating through 'Novelties':
# !!! sort 'Novelties' by 'publication_date' before loop !!! 
def parse_novelty(novelty):   
    preview_message = f'Novelty ID: {novelty.id}'
    report_list = [preview_message]
    # the only difference between 'parse_ua' and 'parse_en' are the model instances being created,
    # the parsing process remains the same
    if novelty.file_path_ua:
        try:
            parsed = parse_ua(novelty)
            if parsed:
                report_list.append(f'{novelty.file_path_ua} was parsed successfully.')
                novelty.parsed_ua = True
                novelty.save()
            else:
                report_list.append(f'Something went wrong parsing \'{novelty.file_path_ua}\'')
        except Exception as e:
            report_list.append(f'Something went wrong parsing \'{novelty.file_path_ua}\'\nException: {e}')
    else:
        report_list.append(f'There\'s no UA post.')
    if novelty.file_path_eng:
        try:
            parsed = parse_en(novelty)
            if parsed:
                report_list.append(f'{novelty.file_path_eng} was parsed successfully.')
                novelty.parsed_eng = True
                novelty.save()
            else:
                report_list.append(f'Something went wrong parsing \'{novelty.file_path_eng}\'')
        except Exception as e:
            report_list.append(f'Something went wrong parsing \'{novelty.file_path_eng}\'\nException: {e}')
    else:
        report_list.append(f'There\'s no EN post.')
    return f'{report_list[0]}\n{report_list[1]}\n{report_list[2]}'



if Novelty.objects.exists():
    for novelty in Novelty.objects.all():
        print(parse_novelty(novelty))
    # test:
    # novelty = Novelty.objects.get(id=9269)
    # print(parse_novelty(novelty))
print('All Done.\n')
    


# # file_ua = 'scrappy_test/pages/downloaded/ua/o-0102231.html'   # 'preview_image/pdf' test
# file_ua = 'scrappy_test/pages/downloaded/ua/o-3112221.html'    # youtube content test    
# file_eng = 'scrappy_test/pages/downloaded/en/eng-3112221.html'
# # file_ua = 'scrappy_test/pages/downloaded/ua/o-3103231.html'
# # file_ua = 'scrappy_test/pages/downloaded/ua/tg-video-test.html'

# # current values ate just hardcoded placeholders to make it run:
# # old_date = '2023-03-31 00:00:00'   # being extracted from novelty page name (provided in the 'novelty' table )
# # indicated_date = '2023-03-31 00:00:00'    # modify this in future - 'YYYY-MM-DD HH:MM:SS.ssssss' format is being used 

# # novelties = Novelty.objects.all()
# # for novelty in novelties:
# #     # ...parse  

# # refactor following code to make it loop through 'Novelties':
# if Novelty.objects.exists():
#     try:
#         novelty = Novelty.objects.first()
#         # exception test:
#         # novelty = Novelty.objects.filter(id=10000)
#         ua_novelty = novelty.file_path_ua
#         en_novelty = novelty.file_path_eng
#         old_date = novelty.publication_date
#         new_date = '20' + old_date
#         formatted_pub_date = datetime.strptime(new_date, '%Y-%m-%d').strftime('%Y-%m-%d')
#         print('*****\nDB Novelty accessed successfully.\n*****')
#         # print(parse_novelty(novelty))
#     except Exception as e:
#         print(f'{e}')
#         sys.exit()
# else:
#     print('Script execution interrupted.')
#     sys.exit()
#     # print('!!!!!\nSomething went wrong. Reading from file.\n!!!!!')
#     # ua_novelty = file_ua
#     # en_novelty = file_eng

# print(novelty)



# # has to be passed while creating the Post model instance:
# admin = User.objects.get(username='admin')

# # All this mess should be commented:
# # migrated_novelty = True

# # the commented one creates new 'NewsList' every run:
# # current_datetime = datetime.now()
# # formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
# # current_datetime = '2023-10-02 21:01:58.194862'

# # newslist = NewsList.objects.get_or_create(
# #     # updated=formatted_datetime,
# #     updated=current_datetime,
# #     source_url_ua='https://www.energoatom.com.ua/news-links.html',
# #     source_url_eng='https://www.energoatom.com.ua/app-eng/news-links.html',
# #     downloaded_ua=True,
# #     downloaded_eng=True,
# #     file_path_ua='scrappy_test/pages/downloaded/ua/news-links.html',
# #     file_path_eng='scrappy_test/pages/downloaded/en/news-links.html',
# # )
# # novelty = Novelty.objects.filter(file_path_ua=file_ua).first()
# # novelty = Novelty.objects.get_or_create(
# #     novelty_url_ua=('https://www.energoatom.com.ua/' + file_ua.split('/')[-1]),
# #     news_list_id=newslist[0],
# #     publication_date='310323',
# #     file_path_ua=file_ua,
# # )

# # Reading the UA 'Novelty' HTML file: 
# with open(file=ua_novelty, mode='r') as file:
#     html_ua = file.read()

# # initializing 'BeautifulSoup' object:
# soup = BeautifulSoup(html_ua, 'html.parser')
# # print(soup)



# content = soup.find('div', class_="col-10 col-sm-8 col-md-10 col-lg-10 col-xl-9 col-xxl-10")
# # print(content)
# extracted_comments = extract_comments(content)
# clean_content = extract_news_links(extracted_comments)

# title = get_exctract_title(clean_content)
# # print(title)
# description = get_exctract_description(clean_content)
# # print(description)

# # now it's time to check whether we have 'preview_image' or video as the first element:
# try:
#     first_element = clean_content.find_all()[0]
#     image_content = first_element.find(name='img', class_='news-img-width')
#     if image_content:   
#         preview_image_path = process_preview_image(image_content)
# except AttributeError as e:
#     print(f'Error appeared during accessing first \'content_block\' element: \n{e}')
# print('----------------------------------------------------------------')

# # after this step I have:
# # - 'title';
# # - 'description';
# # - 'preview_image_path' (saved; if was presented in post);
# print(f'Title: {title}')
# print(f'Description: {description}')
# print('--------------------------------')

# # it's time to proccess the rest of the content block.
# # it may contain images and files.
# try:
#     print('Preview image path:')
#     print(preview_image_path)
# except NameError:
#     print('There\'s no preview image dude')
# print('--------------------------------')



# """
# !!! AT THIS MOMENT I HAVE TO CREATE THE 'POST' INSTANCE
# """
# # print(novelty[0])
# post = Post.objects.get_or_create(
#     meta_title=title,
#     meta_description=description,
#     preview_image=preview_image_path.split('/')[-1],    # there should be only the image file name, I guess.
#     image_alt=image_alt,
#     indicated_date=formatted_pub_date,  
#     added_by=admin,
#     migrated_novelty=True,
#     novelty_id=novelty, 
# )

# # print(post)



# """
# !!! Time to create 'UaPostHead' instance.
# I need for that:
# - 'Post';
# - title;
# - slug = slugify(title);
# - 'preview_text_ua' =  description.
# """
# transliterated_title = translit(title, 'uk', reversed=True)
# slug = slugify(transliterated_title, allow_unicode=True)
# ua_post_head = UaPostHead.objects.get_or_create(
#     post=post[0].id, 
#     title_ua=title, 
#     slug=slug,
#     preview_text_ua=description
# )

# # if both model instances were successfully created report'll be rendered:
# if post:
#     print(f'Post instance: {post}')
# print('--------------------------------')
# if ua_post_head:
#     print(f'UaPostHead instance: {ua_post_head}')
# print('--------------------------------')

# # I'M GOOD!



# # START FROM HERE
# """
# After that I'm 'cleaning' the rest of the content, 
# creating 'UaPostBody' instances during iteration.
# """
# cont_list = clean_content.contents
# cont_list = clear_content_list(cont_list)

# counter = 0
# content_block = []
# content_string = ''
# for i in cont_list:
#     # images:
#     if i.find('img'):
#         img_tag = unwrap_media(i)
#         img_url = img_tag['src']
#         img_name = img_url.split('/')[-1]
#         saved_img_path = download_image(img_name)
#         if saved_img_path:
#             img_tag['src'] = saved_img_path
#         content_block.append(img_tag)
        
#         for item in content_block:
#             content_string += str(item) + '\n'
#         print(content_string)
#         content_string = ''
#         # after that I have to save the'post_body' instance into database
#         counter += 1
        
#         print(f'Block #: {counter}')
#         print(content_block)
#         print('-----')
#         print(saved_img_path)
#         print('######')
#         content_block.clear()
#     # YouTube:
#     elif i.find('iframe'):
#         yt_video_tag = unwrap_media(i)    
#         yt_video_url = yt_video_tag['src']    # works
#         content_block.append(yt_video_tag)
#         # after that I have to save the'post_body' instance into database
#         counter += 1
#         print(f'Block #: {counter}')
#         print(content_block)
#         print('-----')
#         print(yt_video_url)
#         print('######')
#         content_block.clear()
#     # TG video:
#     elif i.find('video'):
#         tg_video_tag = i.find('video')
#         tg_video_url = i.find('video')['src']
#         content_block.append(tg_video_tag)
#         # after that I have to save the'post_body' instance into database
#         counter += 1
#         print(f'Block #: {counter}')
#         print(content_block)
#         print('-----')
#         print(tg_video_url)
#         print('######')
#         content_block.clear()
#     # PDF files:
#     # getting an error trying to download the file
#     # IGNORE FILES FOR NOW:
#     # internal URLs left
#     # ALONG WITH URLs.
#     # elif i.find('a'):
#     #     a_tag = i.find('a')
#     #     url = a_tag['href']
#     #     filename = url.split('/')[-1]
#     #     ext = url.split('.')[-1]
#     #     if ext == 'pdf':
#     #         saved_file_path = download_pdf_file(filename)
#     #         if saved_file_path:        
#     #             a_tag['href'] = saved_file_path 
#     #     content_block.append(a_tag)
#     #     counter += 1
#     #     print(f'Block #: {counter}')
#     #     print(content_block)
#     #     print('-----')
#     #     print(url)
#     #     print('######')
#     #     content_block.clear()
#     else:
#         content_block.append(i)
        


# # print(cont_list)
# print('--------------------------------')
# print(content_block)
# print('--------------------------------')

# links = clean_content.find_all('a') # later on links should be checked 
# tg_videos = clean_content.find_all('video')
# yt_videos = clean_content.find_all('iframe')
# images = clean_content.find_all('img')

# if (len(images) or len(tg_videos) or len(yt_videos)) != 0:
#     print('There\'s some images or videos in the code block')
# elif len(links) != 0:
#     print('There\'s some links in the code block')
# else:
#     print('No attachments in the code block')
# # if len(links) or len(tg_videos) or len(yt_videos) or len(images) != 0:
# #     for tag in clean_content.contents:
# #         pass

# print(links)
# print(tg_videos)
# print(yt_videos)
# print(images)

# # print(title)
# # print(description)
# # print(content.prettify)
# # print(preview_image)
# # print(clean_content.find_all())



# # print('###############')
# # # print(clean_content.find_all()[0].name)
# # print(first_element.name)
# # print('###############')





# # # gets and excludes 'description' from 'section' to store it in the variable:
# # def get_extract_description(section):
# #     description = section.find(name='p', class_='single-description')
# #     return description
    
# # 'title' and 'description' go to 'Ua/EnPostHead':
# # title = get_exctract_title(clean_section)
# # description = get_extract_description(clean_section)
# # title = clean_section.find('h1', class_='single-title')
# # description = clean_section.find(name='p', class_='single-description')
# # title_parent_div = title.find_parent('div', class_='row justify-content-center')



# # section = get_section(soup)
# # clean_section = exclude_comments(section)

# # more precise than the whole '<section>':
# # content = soup.find('div', class_="col-10 col-sm-8 col-md-10 col-lg-10 col-xl-9 col-xxl-10")

# # clean_content = extract_comments(content)
# # clean_content = extract_news_links(clean_content)

# # this one checks if first element of the contects list is vidoe or not
# # (has to be modifiesd; it's just a robust scheme)
# # ((this is going to run functions to manipulate with image/video))
# # contents = clean_content.contents
# # while '\n' in contents:
#     # contents.remove('\n')    
# # print(contents)
# # for item in contents:
#     # print(item)
# # print(contents.find_all('p'))
# # print('######')
# # if contents[0].find('iframe'):
#     # print('video found')
# # else:
#     # print(contents[0].find('img'))
# # print('######')

    
# # it handles 'img' path replacement:
# # img_tag = clean_content.find(name='img', class_='news-img-width')
# # I'll need this to 'extract' the whole preview image's tag from the 'clean_content':
# # img_parent = img_tag.find_parent('div', class_='d-flex justify-content-center pb-5')
# # print(img_parent)

# # img_tag['src'] = './images/dist/bg-photo/photo-0102231.png'
# # filename = img_tag['src'].split('/')[-1]
# # image_url = photo_base_uri + filename



# # # Ensure the download directory exists, create it if necessary (later);
# # response = requests.get(image_url)
# # if response.status_code == 200:
# #     save_path = os.path.join(os.path.abspath('..'), image_path, filename)
# #     with open(save_path, 'wb') as file:
# #         file.write(response.content)
# #     print(f"Image '{filename}' downloaded and saved to '{save_path}'")
# #     img_parent.extract()
# # else:
# #     print(f"Failed to download image from '{image_url}', status code: {response.status_code}")

# # # searches for links in the rest of cleaned content:
# # if clean_content.find_all('a'):
# #     for child in clean_content.children:
# #         if child.name == 'p':
# #             a_tag = child.css.select("p > a")
# #             if a_tag:
# #                 # a_tag
# #                 print(a_tag[0]['href'])
# # else:
# #     print(False)


