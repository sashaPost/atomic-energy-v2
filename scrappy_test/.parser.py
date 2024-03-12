from bs4 import BeautifulSoup, Comment
import calendar
from django.contrib.auth.models import User
from django.db.models import Q
import os
import random
import requests
import re
from requests.exceptions import RequestException
import time

from scrappy_test.models import NewsList, Novelty

import pdb
from django.shortcuts import render




base_url = 'https://www.energoatom.com.ua'
photo_base_uri = 'https://www.energoatom.com.ua/images/dist/bg-photo/'
pdf_base_uri = 'https://www.energoatom.com.ua/parts/pdf-file/'

newslist_url_ua = 'https://www.energoatom.com.ua/news-links.html'    # 2023
newslist_url_eng = 'https://www.energoatom.com.ua/app-eng/news-links.html'    # 2023
newslist_url_old_ua = 'https://www.energoatom.com.ua/news-links-2022.html'
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



# parsing Novelties:
def download_image(image_url):
    pass

def extract_image_path(image_src):
    img_name = image_src.split('/')[-1]
    return base_url + '/images/dist/bg-photo/' + img_name

def deownload_pdf(url, dir):
    pass

def check_pdf(filename):
    extension = filename.split('.')[-1].lower()
    if extension == 'pdf':
        return True
    return False
    
def check_html(filename):
    extension = filename.split('.')[-1].lower()
    if extension == 'html':
        return True
    return False
    
# This one works correct.
# Implement all the modifications here.
def novelty_parse(request):
    
    # has to be passed while creating the Post model instance
    admin = User.objects.get(username='admin')
    
    # !!!FORGOT ABOUT SEO TAGS!!!   # solved
    # <meta name="description" content="!!!" to Post.meta_description
    
    novelties = Novelty.objects.all()
    missing_ids = []
    contents = {}
    
    for novelty in novelties:
        
        # working on UA file first
        # all Model fields can't be filled on this step, 
        # should be nullable and have default value
        if novelty.file_path_ua:
            pub_date = novelty.publication_date
            
            url_ua = novelty.novelty_url_ua
            file_path_ua = novelty.file_path_ua
            
            context = {}
            context['novelty_id'] = novelty.id
            print(f"novelty_id: {context['novelty_id']}")
            
            try:
                with open(file=file_path_ua, mode='r') as file:
                    html_ua = file.read()
                
                soup_ua = BeautifulSoup(markup=html_ua, features='html.parser')
                
                context['added_by'] = admin
                
                # getting the <meta name="description"> tag,
                # maybe should get the value of 'content'
                meta_description = soup_ua.find(name='meta', attrs={'name': 'description'})
                if meta_description:
                    meta_tag = meta_description['content']
                    context['meta_description'] = meta_tag
                    print(f"meta_description: {context['meta_description']}")
                
                # selecting the element containing all the needed post data
                section_ua = soup_ua.find('section', class_='single')
                if section_ua:
                    context['section_ua'] = section_ua
                    
                    # excluding the data unrelated to post:
                    unwanted_ul = section_ua.find('ul', class_='sidebar-body')
                    if unwanted_ul:
                        unwanted_ul.extract()
                                        
                    # getting rid off the comments:
                    comments = section_ua.find_all(text=lambda text: isinstance(text, Comment)) 
                    if comments:
                        for comment in comments:
                            comment.extract()                
                    
                    title_ua = section_ua.find(name='h1', class_='single-title')
                    if title_ua:
                        title_ua.extract()
                        context['title_ua_content'] = title_ua.text.strip()
                        print(f"title_ua: {context['title_ua_content']}")
                    
                    preview_ua = section_ua.find(name='p', class_='single-description')
                    if preview_ua:
                        preview_ua.extract()
                        context['preview_ua_content'] = preview_ua.text.strip()
                        print(f"preview_text_ua: {context['preview_ua_content']}")
                        
                    # section allows to get image URL from the Novelty                        
                    images = section_ua.find_all(name='img', class_='news-img-width')
                    if images:
                        preview_image_src = images[0]['src']
                        preview_image_url = extract_image_path(image_src=preview_image_src)
                        # download image using 'preview_image_url'
                        # section_ua.find(name='img', class_='news-img-width') = preview_image_url
                        context['preview_image_url'] = preview_image_url
                        print(f"preview_image_url: {context['preview_image_url']}")   
                        images[0]['src'] = preview_image_url     # this line changed the source for the preview image                      
                        
                        context['novelty_images_urls'] = [ img_src['src'] for img_src in images[1:] ]
                        if context['novelty_images_urls']:
                                                        
                            for i in range(len(context['novelty_images_urls'])):
                                # src = extract_image_path(image_src=src)
                                new_img_url = extract_image_path(image_src=context['novelty_images_urls'][i])
                                context['novelty_images_urls'][i] = new_img_url
                                images[i + 1]['src'] = new_img_url # this line changed the source for the Novelty images
                                # pdb.set_trace()
                            print(f"novelty_images_urls: {context['novelty_images_urls']}")
                        
                            print('-----')
                        print(f'images: {images}')
                    print('-----')
                    
                    paragraphs = section_ua.find_all(name='p', class_='single-paraph')
                    if paragraphs:
                        for paragraph in paragraphs:
                            attachments = paragraph.find(name='a')
                            # attachments = paragraph['a']
                            
                            if attachments:
                                context['attachments'] = attachments['href']
                                filename = attachments['href'].split('/')[-1].lower()
                                if check_pdf(filename):
                                    # download the file
                                    # replace the link
                                    pass
                                
                                if check_html(filename):
                                    
                                    pass
                                print(f"attachments: {attachments['href']}")         
                                
                                #!!!ATTACHMENTS AS WELL AS THE OTHER ELEMENTS (CHECK) SHOULD BE TRANSFERRED WITH STYLIZATION
                                # write a function to check if URL belongs to 'energoatom.com.ua'
                                    # if so, extract 'novelty_id' from URL and search for it:
                                    # mysql> select * from scrappy_test_novelty where novelty_url_ua like '%2806221%';
                                    # novelties = Novelty.objects.filter(novelty_url_ua__contains='2806221')
                                
                                # write a function to check if URL contains a file
                                    # download this
                                    
                                # if none of the rules worked, just transfer the URL
                    
                    print('-----')
                    print(f"section: {context['section_ua']}")
                    
                    contents[str(novelty.id)] = context
                    
                    
                    
                # perform appropriate manipulations with 'section_ua':
                    # - find the image files names;
                    # - compose the link for image download;
                    # - download images, save the model instance, change path in html;  HOW TO SAVE THE PostImages WITHOUT SAVING Post???
                    # - perform the same operations for the attached files;                  
                # perform checks if post has images and attached files
                # if novelty.file_path_eng:
                #     url_en = novelty.novelty_url_eng
                #     file_path_en = novelty.file_path_eng
                #     # just a test
                #     print(f'UA: {file_path_ua}; EN: {file_path_en}\n')
                #     print('\n')
                # just a test
                # print(f'UA: {file_path_ua}\nNo English version provided.\n')
                # print('\n')
                # try:
                #     print(context['novelty_images'])
                # except KeyError as e:
                #     print(e)
                
                print('\n#####')
                                        
            except FileNotFoundError as e:
                if novelty.id not in missing_ids:
                    missing_ids.append(novelty.id)
                print(f'{e}')
                
        else:
            if novelty.id not in missing_ids:
                missing_ids.append(novelty.id)
            print(f'Novelty ID {novelty.id} file is is missing.\n')
    
    print(f'Missed Novelty IDs: {missing_ids}')
    return render(request=request, template_name='scrappy_test/test.html', context={'contents': contents})
    

# def novelty_parse_test():
    
#     # file_id = '0505233'
#     file_id = '0102231'
    
#     # novelty = Novelty.objects.latest('id')
#     novelty = Novelty.objects.filter(novelty_url_ua__contains=file_id)
#     url_ua = novelty[0].novelty_url_ua
#     file_ua = novelty[0].file_path_ua
    
#     # novelty_ua = novelty.file_path_ua
#     # novelty_en = novelty.file_path_eng
    
#     with open(file=file_ua, mode='r') as file:
#         html_ua = file.read()
        
#     soup_ua = BeautifulSoup(markup=html_ua, features='html.parser')
#     # title_ua = soup_ua.find('h1', class_='single-title').text.strip()
#     # description_ua = soup_ua.find('p', class_='single-description') 
#     section = soup_ua.find('section', class_='single')
#     # section_elements = [ element for element in section ]
    
    
#     # image_pb = soup_ua.find('div', class_='d-flex justify-content-center pb-5')    # add "d-flex justify-content-center pt-5"; findall
#     images = section.find_all('img', class_='news-img-width')    # print(image_list[0]['src'])
#     if images:
#         # img_names = [ image['src'].split('/')[-1] for image in images ]
#         # img_urls = [ photo_base_uri + img for img in img_names ] 
#         for image in images:
#             image_name = image['src'].split('/')[-1]
#             image_url = photo_base_uri + image_name
#             # result 
#             download_image(image_url=image_url)    # must return saved image path
#             print(image_url)    # just a test
    
#     # text = soup_ua.get_text()
    
#     # to get rid off the '<ul class="sidebar-body">'
#     unwanted_ul = section.find('ul', class_='sidebar-body')
#     if unwanted_ul:
#         unwanted_ul.extract()
    
#     # with open(file=novelty.file_path_eng, mode='r') as file:
#     #     html_en = file.read()
    
#     # for element in soup_ua:
#     #     print(element)
    
#     attachments = []
#     paragraphs = section.find_all('p', class_='single-paraph')
#     if paragraphs:
#         for paragraph in paragraphs:
#             try:
#                 # download the file from the 'attachment_path',
#                 # change the value of 'paragraph.find('a').get('href')' to a local path in the filesystem.
#                 # make changes to the database (allow to the file upload to Post).
#                 attachment_path = base_url + paragraph.find('a').get('href')
#             except AttributeError as e:
#                 pass
                                
    
#     for image, url in zip(images, img_urls):
#         src = image['src']
#         src = url
#         print(src)
        
#     # containers = soup_ua.find_all(name='div', class_='container')    # test code
        
#     return attachments



# for 'Novelty':
def soup(html_file):
    """_summary_

    Args:
        html_file (_type_)

    Returns:
        _type_: list
    """
    soup = BeautifulSoup(markup=html_file, features='html.parser')    
    a_elements = soup.find_all(name='a', class_='theses-item-link')
    hrefs = [ a.get('href') for a in a_elements ]
    return hrefs    

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

def extract_UA_novelty_urls(newslist_file_ua, newslist):
    """
    accepts html page (NewsList), puts novelty urls into database
    """
    hrefs = soup(newslist_file_ua)
    list_of_dates = extract_dates(list_of_urls=hrefs)
    for novelty_url, date in zip(hrefs, list_of_dates):
        full_url_ua = base_url + novelty_url
        try:
            novelty = Novelty.objects.get(novelty_url_ua=full_url_ua)
        except Novelty.DoesNotExist as e:    
            novelty = Novelty.objects.get_or_create(novelty_url_ua=full_url_ua, news_list_id=newslist, publication_date=date)
            newslist.parsed_ua = True
            newslist.save()

def extract_EN_novelty_urls(newslist_file_en, newslist):
    hrefs = soup(html_file=newslist_file_en)
    
    newslist_novelties = newslist.novelty_set.all()
    news_nov_urls_ua = [ smth.novelty_url_ua for smth in newslist_novelties ]
    
    for en_url in hrefs:
        en_url_id = get_novelty_id(novelty_url=en_url)
        for ua_url in news_nov_urls_ua:
            if en_url_id in ua_url:
                full_url_en = base_url + en_url
                novelty = Novelty.objects.get(novelty_url_ua=ua_url)
                novelty.novelty_url_eng = full_url_en
                novelty.save()            
            else:
                novelty = Novelty.objects.get(novelty_url_ua=ua_url)
                novelty.novelty_url_eng = False
                novelty.save()

def parse_newslists():
    newslists = NewsList.objects.all()
    # print(newslists)
    for lst in newslists:
        # print(lst.file_path_ua, lst.file_path_eng)
        with open(file=lst.file_path_ua, mode='r') as file:
            html_ua = file.read()
        
        with open(file=lst.file_path_eng, mode='r') as file:
            html_eng = file.read()
        
        extract_UA_novelty_urls(newslist_file_ua=html_ua, newslist=lst)
        extract_EN_novelty_urls(newslist_file_en=html_eng, newslist=lst)
    return 'Done.'
        
        
        
# test this two in the morning:
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
    novelties = Novelty.objects.all()
    if novelties:
        for novelty in novelties:
            # print(init_delay())
            if novelty.file_path_ua == None:
                if novelty.novelty_url_ua.split('/')[-1] == 'paes-2905231.html':
                    continue
                else:
                    try:
                        print(download_novelty_html(url=novelty.novelty_url_ua, dir=path_ua))
                        novelty.downloaded_ua = True
                        novelty.file_path_ua = path_ua + novelty.novelty_url_ua.split('/')[-1]
                        novelty.save()
                        print(init_delay())
                    except RequestException as e:
                        return f'Error occurred during the download: {str(e)}'
            
            if novelty.novelty_url_eng:
                if novelty.file_path_eng == None:
                    try:
                        print(download_novelty_html(url=novelty.novelty_url_eng, dir=path_en))
                        novelty.downloaded_eng = True
                        novelty.file_path_eng = path_en + novelty.novelty_url_eng.split('/')[-1]
                        novelty.save()
                        print(init_delay())
                    except RequestException as e:
                        return f'Error occurred during the download: {str(e)}'
    return 'Nothing left to download.'        



# 'NewsList' manipulations:
def source_urls_create():
    """
    fills the database with the source links (news lists).
    (run from the shell)
    """
    # creates the source links for the news lists (all years and months, including 'eng')
    sources_ua_2023 = [ (newslist_url_ua + '#' + month) for month in month_names ]
    sources_ua_2023.insert(0, newslist_url_ua)
    sources_eng_2023 = [ (newslist_url_eng + '#' + month) for month in month_names ]
    sources_eng_2023.insert(0, newslist_url_eng)
    old_sources_ua = [ (newslist_url_old_ua + '#' + month) for month in month_names ]
    old_sources_ua.insert(0, newslist_url_old_ua)
    old_sources_eng = [ (newslist_url_old_eng + '#' + month) for month in month_names ]
    old_sources_eng.insert(0, newslist_url_old_eng)
    
    source_links_ua = sources_ua_2023 + old_sources_ua
    source_links_eng = sources_eng_2023 + old_sources_eng
    
    for ukr_link, eng_link in zip(source_links_ua, source_links_eng):
        newslist = NewsList.objects.get_or_create(source_url_ua=ukr_link, source_url_eng=eng_link)
        print(f'News list {newslist[0].id} created')
    
    return 'Done'

def download_newslist_html(dir, url):
    try:
        filename = url.split('/')[-1]
        response = requests.get(url)     
        if response.status_code == 200:   
            file_path = os.path.join(dir, filename)
            with open(file_path, 'w') as file:
                file.write(response.text)
    except RequestException as e:
        return f'Error occurred during the download: {str(e)}'
    
def newslist_download(record):
    """
    Downloads both 'ua' and 'eng' versions of the news lists pages from the database.
    """
    if not os.path.exists(path_ua) or not os.path.exists(path_en):
        os.makedirs(name=path_ua, exist_ok=True)
        os.makedirs(name=path_en, exist_ok=True)
    
    if record.downloaded_ua == False:
        download_newslist_html(path_ua, record.source_url_ua)
        record.downloaded_ua = True
        record.file_path_ua = path_ua + record.source_url_ua.split('/')[-1]
        record.save()
        print(f'{record.source_url_ua} was just saved.')
            
        delay = random.randint(7, 13)
        time.sleep(delay)
        print(f'inner delay: {delay}s')
        
    if record.downloaded_eng == False:
        download_newslist_html(path_en, record.source_url_eng)
        record.downloaded_eng = True
        record.file_path_eng = path_en + record.source_url_eng.split('/')[-1]
        record.save()
        print(f'{record.source_url_eng} was just saved.') 
    return f'Record ID: {record.id} was updated.'    # specify the page
    
def trigger_newslist_download():
    """
    asynchronously triggers 'download_newslist_html_ua()' allowing to download list of HTML pages 
    using previously generated pages URLs in database
    """
    db_records = NewsList.objects.filter(Q(downloaded_ua=False) | Q(downloaded_eng=False))
    if db_records:
        for record in db_records:
            delay = random.randint(13, 39)
            time.sleep(delay)
            print(f'Delay: {delay}s')
            print(newslist_download(record=record))
            return trigger_newslist_download()
    return 'Nothing to download.'

def check_newslist_download():
    """
    Checks if the news list HTML file is persisted on the filesystem. 
    """
    # db_records = NewsList.objects.filter(Q(downloaded_ua=False) | Q(downloaded_eng=False))
    db_records = NewsList.objects.all()
    if db_records:
        for record in db_records:
            filename_ua = record.source_url_ua.split('/')[-1]
            filepath_ua = os.path.join(path_ua, filename_ua)
            
            filename_en = record.source_url_eng.split('/')[-1]
            filepath_en = os.path.join(path_en, filename_en)
            
            if os.path.exists(filepath_ua):
                record.downloaded_ua = True
                record.file_path_ua = filepath_ua
                record.save()
            else:
                print(f'{filename_ua} doesn\'t exist') 
            
            if os.path.exists(filepath_en):
                record.downloaded_eng = True
                record.file_path_eng = filepath_en
                record.save()
            else:
                print(f'{filename_en} doesn\'t exist')
                
    return '\nDone.'



# helper function:
def counter():
    both = Novelty.objects.count()
    
    en_count = 0
    test = Novelty.objects.all()
    for en in test:
        if en.novelty_url_eng:
            en_count += 1
    return (both + en_count)