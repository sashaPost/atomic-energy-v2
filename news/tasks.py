from celery import shared_task
import requests
from news.models import Post, UaPostBody, EnPostBody
import os
import logging
from dotenv import load_dotenv



load_dotenv('.env')
API_KEY = os.getenv('API_KEY')  

logger = logging.getLogger(__name__)

# logger.info('API_KEY: %s', API_KEY)

# triggers if existing Post's 'preview_image' is being updated:
@shared_task
def send_preview_image(post_id):
    logger.info(f"'send_preview_image()' was triggered")
    logger.info('API_KEY: %s', API_KEY)
    media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
    logger.info(f"Post ID processed by task: {post_id}")
    try:
        post = Post.objects.get(pk=post_id)
        if post.preview_image:
            image_path = post.preview_image.path
            image_filename = os.path.basename(image_path)
            url = media_host_url + image_filename

            headers = {
                'Authorization': f'{API_KEY}',
                # 'Content-Type': 'image/jpeg',
            }
            with open(image_path, 'rb') as image_file:
                response = requests.post(url, files={'file': image_file}, headers=headers)    
                if response.status_code == 200:
                    logger.info(f'Post ID {post_id} preview image was sent to media host!')
                    return True
                else:
                    logger.error('Sending image to media host failed:', response.status_code)
                    return False
        logger.warning(f"Post ID {post_id} seems to have no 'preview_image'")
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
            logger.info(f'UaPostBody ID {post_body.id} image was sent to media host!')
            return True
        else:
            logger.error(f"Sending UaPostBody ID {post_body.id} image to media host failed: {response.status_code}")
            return False

# being called if 'Ua/EnPostBody' image was updated:
# (triggers 'process_body_image)
@shared_task
def send_body_img(post_body_id, lang):
    logger.info(f"'send_body_img()' was triggered")
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


# triggers if new Post instance is being created:
@shared_task
def send_media(post_id):
    logger.info(f"'send_media()' was triggered")
    media_host_url = os.getenv('MEDIA_HOST_IMAGES_URL')
    # media_host_url = 'https://old.energoatom.com.ua/media/images/'
    logger.info(f"Post ID processed by task: {post_id}")
    try:
        headers = {'Authorization': f'{API_KEY}'}
        
        post = Post.objects.get(pk=post_id)
        if post.preview_image:
            image_path = post.preview_image.path
            image_filename = os.path.basename(image_path)
            url = media_host_url + image_filename

            with open(image_path, 'rb') as image_file:
                response = requests.post(url, files={'file': image_file}, headers=headers)    
                if response.status_code == 200:
                    logger.info('Post preview image was sent to media host!')
                else:
                    logger.error('Sending image to media host failed:', response.status_code)
                
        ua_post_bodies = post.ua_body.all()
        for ua_post_body in ua_post_bodies:
            if ua_post_body.image:
                image_path = ua_post_body.image.path
                image_filename = os.path.basename(image_path)
                url = media_host_url + image_filename

                with open(image_path, 'rb') as image_file:
                    response = requests.post(url, files={'file': image_file}, headers=headers)    
                    if response.status_code == 200:
                        logger.info('UaPostBody image was sent to media host!')
                    else:
                        logger.error('Sending image to media host failed:', response.status_code)

        en_post_bodies = post.en_body.all()
        for en_post_body in en_post_bodies:
            if en_post_body.image:
                image_path = en_post_body.image.path
                image_filename = os.path.basename(image_path)
                url = media_host_url + image_filename

                with open(image_path, 'rb') as image_file:
                    response = requests.post(url, files={'file': image_file}, headers=headers)    
                    if response.status_code == 200:
                        logger.info('EnPostBody image was sent to media host!')
                    else:
                        logger.error(f"Sending image to media host failed: {response.status_code}")
        return True
        
    except Exception as e:
        logger.error(f'Error sending an image: {e}')
        return False