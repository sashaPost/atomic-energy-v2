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

from news.models import *
from scrappy_test.models import *
from scrappy_test.novelty_help_func import *
from django.contrib.auth.models import User

from slugify import slugify
from transliterate import translit



image_alt = 'Broken image placeholder.'

def parse_ua_body(content, novelty):
    """
    'cleaning' the rest of  content, 
    creating 'UaPostBody' instances during iteration
    through 'content list'.
    """
    image_alt = 'Broken image placeholder.'
    
    cont_list = content.contents
    cont_list = remove_n_and_css(cont_list)

    counter = 0
    content_block = []
    content_string = ''
    
    post = get_post_using_novelty(novelty)
    
    for i in cont_list:
        # images:
        if i.find('img'):
            saved_img = process_image_with_tag(i)
            if saved_img:
                i['src'] = saved_img['path']
            content_block.append(i)
            
            for item in content_block:
                content_string += str(item) + '\n'
            # print(content_string)
            content_block.clear()
            
            ua_post_body = UaPostBody.objects.get_or_create(
                post = post,
                message_ua = content_string,
                image = saved_img['path'],
                post_image_alt = image_alt,
                # there's no 'video_url' if 'PostBody' image is being processed:
                video_url = False,
            )            
            # print(ua_post_body)
            counter += 1
            content_string = ''
        # YouTube:
        elif i.find('iframe'):
            yt_video_tag = unwrap_media(i)    
            yt_video_url = yt_video_tag['src']    # works
            content_block.append(yt_video_tag)
            
            for item in content_block:
                content_string += str(item) + '\n'
            content_block.clear()
            
            image_alt = 'Model instance has no image.'
            
            ua_post_body = UaPostBody.objects.get_or_create(
                post = post,
                message_ua = content_string,
                image = False,
                post_image_alt = image_alt,
                video_url = yt_video_url,
            )           
                
            counter += 1
            content_string = ''
        # TG video:
        elif i.find('video'):
            tg_video_tag = i.find('video')
            tg_video_url = i.find('video')['src']
            content_block.append(tg_video_tag)

            for item in content_block:
                content_string += str(item) + '\n'
            content_block.clear()
            
            image_alt = 'Model instance has no image.'
            
            ua_post_body = UaPostBody.objects.get_or_create(
                post = post,
                message_ua = content_string,
                image = False,
                post_image_alt = image_alt,
                video_url = tg_video_url,
            )           
            
            counter += 1
            content_string = ''
            
        # !!! DO THIS LATER !!!
        # PDF files:
        # getting an error trying to download the file
        # IGNORE FILES FOR NOW:
        # internal URLs left
        # ALONG WITH URLs.
        # elif i.find('a'):
        #     a_tag = i.find('a')
        #     url = a_tag['href']
        #     filename = url.split('/')[-1]
        #     ext = url.split('.')[-1]
        #     if ext == 'pdf':
        #         saved_file_path = download_pdf_file(filename)
        #         if saved_file_path:        
        #             a_tag['href'] = saved_file_path 
        #     content_block.append(a_tag)
        #     counter += 1
        #     print(f'Block #: {counter}')
        #     print(content_block)
        else:
            content_block.append(i)
            # counter += 1
    
    if len(content_block) > 0:        
        for item in content_block:
            content_string += str(item) + '\n'
        content_block.clear()
                        
        image_alt = 'Model instance has no image or video.'
        
        ua_post_body = UaPostBody.objects.get_or_create(
            post = post,
            message_ua = content_string,
            image = False,
            post_image_alt = image_alt,
            video_url = False,
        )     
        
        counter += 1
        content_string = ''
            
    return post.ua_body.all()

def parse_ua_head(novelty):
    # has to be passed while creating the Post model instance:
    admin = User.objects.get(username='admin')
    # image_alt = 'Broken image placeholder.'
    novelty_html = novelty.file_path_ua
    # print(novelty_html)
    old_date = novelty.publication_date
    new_date = '20' + old_date
    formatted_pub_date = datetime.strptime(new_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    # print(formatted_pub_date)
    soup = create_soup(novelty_html)
    # print(soup)
    content = soup.find('div', class_="col-10 col-sm-8 col-md-10 col-lg-10 col-xl-9 col-xxl-10")
    # print(content)
    extracted_comments = extract_comments(content)
    # print(extracted_comments)
    clean_content = extract_news_links(extracted_comments)
    # print(clean_content)
    title = get_exctract_title(clean_content)
    if title:
        title = title.strip()
    # print(title)
    description = get_exctract_description(clean_content)
    if description:
        description = description.strip()
    # print(description)
    preview_image = get_extract_preview_image(clean_content)
    # print(preview_image)
    
    preview_image_pd_path = None
    if not preview_image:
        preview_image = None
        preview_image_pd_path = None
    else:
        preview_image_bd_path = os.path.join('images', preview_image)
    # print(preview_image)
        
    category = get_category()
        
    # test:
    # novelty_id = novelty.id
    # print(novelty_id)
    
    # !!! fix 'title' and 'description' !!!
    post = Post.objects.get_or_create(
        meta_title=title,
        meta_description=description,
        preview_image=preview_image_bd_path,
        image_alt=image_alt,
        indicated_date=formatted_pub_date,  
        added_by=admin,
        migrated_novelty=True,
        novelty_id=novelty, 
        old_date=formatted_pub_date,
        category=category,
    )
    # Now it's time to create 'UaPostHead' instance. 
    transliterated_title = translit(title, 'uk', reversed=True)
    slug = slugify(transliterated_title, allow_unicode=True)
    ua_post_head = UaPostHead.objects.get_or_create(
        post=post[0], 
        title_ua=title, 
        slug=slug,
        preview_text_ua=description
    )

    if post and ua_post_head:
        return {
            'post': post[0],
            'ua_post_head': ua_post_head[0],
            'clean_content': clean_content,
        }
    else:
        False
        
def parse_ua(novelty):
    ua_post_head = parse_ua_head(novelty)
    post_body_content = ua_post_head['clean_content']
    ua_post_body = parse_ua_body(post_body_content, novelty)
    if ua_post_head and ua_post_body:
        return {
            'ua_post_head': ua_post_head,
            'ua_post_body': ua_post_body,
        }
    else:
        return False

