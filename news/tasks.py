from celery import shared_task
import requests
from news.models import UaPostHead, EnPostHead, UaPostBody, EnPostBody
import os
import logging
from dotenv import load_dotenv



load_dotenv('.env')
API_KEY = os.getenv('API_KEY')  

logger = logging.getLogger(__name__)

# logger.info('API_KEY: %s', API_KEY)

def process_head_image(post_head):
    logger.info(f"!!! 'process_head_image()' task was triggered !!!")
    logger.info(f"'post_head': {post_head}")
    media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
    image_path = post_head.preview_image.path
    logger.info(f"'image_path': {image_path}")
    image_filename = os.path.basename(image_path)
    url = media_host_url + image_filename
    logger.info(f"Request URL: {url}")
    headers = {'Authorization': f'{API_KEY}'}
    with open(image_path, 'rb') as image_file:
        response = requests.post(url, files={'file': image_file}, headers=headers)    
        if response.status_code == 200:
            logger.info(f'PostHead ID {post_head.id} image was sent to media host!')
            return True
        else:
            logger.error(f"Sending PostHead ID {post_head.id} image to media host failed: {response.status_code}")
            return False
        
@shared_task
def send_head_img(post_head_id, lang):
    logger.info(f"'!!! send_head_img()' task was triggered !!!")
    logger.info(f"PostHead ID processed by task: {post_head_id}")
    logger.info(f"lang: {lang}")
    try:
        if lang == 'UA':
            ua_post_head = UaPostHead.objects.get(pk=post_head_id)
            logger.info(f"UaPostHead with ID {post_head_id} exists: {ua_post_head}")
            if ua_post_head.preview_image:
                if process_head_image(ua_post_head):
                    return True
                return False
            logger.info(f"UaPostHead ID {post_head_id} seems to have no 'image'")
            return False

        if lang == 'EN':
            en_post_head = EnPostHead.objects.get(pk=post_head_id)
            logger.info(f"EnPostHead with ID {post_head_id} exists: {en_post_head}")
            if en_post_head.preview_image:
                if process_head_image(en_post_head):
                    return True
                else:
                    return False
            logger.info(f"UaPostHead ID {post_head_id} seems to have no 'image'")
            return False
    except Exception as e:
        logger.error(f'Error sending an image: {e}')
        return False

# sends body image to media host:
def process_body_image(post_body):
    logger.info(f"'process_body_image()' was triggered")
    media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
    image_path = post_body.image.path
    image_filename = os.path.basename(image_path)
    url = media_host_url + image_filename

    headers = {'Authorization': f'{API_KEY}'}
    with open(image_path, 'rb') as image_file:
        response = requests.post(url, files={'file': image_file}, headers=headers)    
        if response.status_code == 200:
            logger.info(f'PostBody ID {post_body.id} image was sent to media host!')
            return True
        else:
            logger.error(f"Sending PostBody ID {post_body.id} image to media host failed: {response.status_code}")
            return False
            
# being called if 'Ua/EnPostBody' image was updated:
# (triggers 'process_body_image)
@shared_task
def send_body_img(post_body_id, lang):
    logger.info(f"'send_body_img()' task was triggered")
    # media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
    logger.info(f"PostBody ID processed by task: {post_body_id}")
    try:
        if lang == 'UA':
                post_body = UaPostBody.objects.get(pk=post_body_id)
                if post_body.image:
                    if process_body_image(post_body):
                        return True
                    return False
                logger.info(f"UaPostBody ID {post_body_id} seems to have no 'image'")
                return False

        if lang == 'EN':
                post_body = EnPostBody.objects.get(pk=post_body_id)
                if post_body.image:
                    if process_body_image(post_body):
                        return True
                    else:
                        return False
                logger.info(f"UaPostBody ID {post_body_id} seems to have no 'image'")
                return False
    except Exception as e:
        logger.error(f'Error sending an image: {e}')
        return False



# # !!! rewrite this:
# # triggers if existing Post's 'preview_image' is being updated:
# @shared_task
# def send_preview_image(post_id):
#     logger.info(f"'send_preview_image()' was triggered")
#     logger.info('API_KEY: %s', API_KEY)
#     media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
#     logger.info(f"Post ID processed by task: {post_id}")
#     try:
#         post = Post.objects.get(pk=post_id)
#         if post.preview_image:
#             image_path = post.preview_image.path
#             image_filename = os.path.basename(image_path)
#             url = media_host_url + image_filename

#             headers = {
#                 'Authorization': f'{API_KEY}',
#                 # 'Content-Type': 'image/jpeg',
#             }
#             with open(image_path, 'rb') as image_file:
#                 response = requests.post(url, files={'file': image_file}, headers=headers)    
#                 if response.status_code == 200:
#                     logger.info(f'Post ID {post_id} preview image was sent to media host!')
#                     return True
#                 else:
#                     logger.error('Sending image to media host failed:', response.status_code)
#                     return False
#         logger.warning(f"Post ID {post_id} seems to have no 'preview_image'")
#         return False
#     except Exception as e:
#         logger.error(f'Error sending an image: {e}')
#         return False

# !!! rewrite this one as well:
# triggers if new Post instance is being created:
# @shared_task
# def send_media(post_id):
#     logger.info(f"'send_media()' was triggered")
#     media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
#     # media_host_url = 'https://old.energoatom.com.ua/media/images/'
#     logger.info(f"Post ID processed by task: {post_id}")
#     try:
#         headers = {'Authorization': f'{API_KEY}'}
        
#         post = Post.objects.get(pk=post_id)
#         if post.preview_image:
#             image_path = post.preview_image.path
#             image_filename = os.path.basename(image_path)
#             url = media_host_url + image_filename

#             with open(image_path, 'rb') as image_file:
#                 response = requests.post(url, files={'file': image_file}, headers=headers)    
#                 if response.status_code == 200:
#                     logger.info('Post preview image was sent to media host!')
#                 else:
#                     logger.error('Sending image to media host failed:', response.status_code)
                
#         ua_post_bodies = post.ua_body.all()
#         for ua_post_body in ua_post_bodies:
#             if ua_post_body.image:
#                 image_path = ua_post_body.image.path
#                 image_filename = os.path.basename(image_path)
#                 url = media_host_url + image_filename

#                 with open(image_path, 'rb') as image_file:
#                     response = requests.post(url, files={'file': image_file}, headers=headers)    
#                     if response.status_code == 200:
#                         logger.info('UaPostBody image was sent to media host!')
#                     else:
#                         logger.error('Sending image to media host failed:', response.status_code)

#         en_post_bodies = post.en_body.all()
#         for en_post_body in en_post_bodies:
#             if en_post_body.image:
#                 image_path = en_post_body.image.path
#                 image_filename = os.path.basename(image_path)
#                 url = media_host_url + image_filename

#                 with open(image_path, 'rb') as image_file:
#                     response = requests.post(url, files={'file': image_file}, headers=headers)    
#                     if response.status_code == 200:
#                         logger.info('EnPostBody image was sent to media host!')
#                     else:
#                         logger.error(f"Sending image to media host failed: {response.status_code}")
#         return True
        
#     except Exception as e:
#         logger.error(f'Error sending an image: {e}')
#         return False