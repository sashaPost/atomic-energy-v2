from celery import shared_task
from .models import Procurement
import requests
import os
from dotenv import load_dotenv
import logging



load_dotenv('.env')

logger = logging.getLogger(__name__)

@shared_task
def send_doc_file_to_media_host(procurement_id):
    media_host_url = os.getenv('MEDIA_HOST_FILES_URL')    
    logger.info(media_host_url)
    
    procurement = Procurement.objects.get(id=procurement_id)
    logger.info(procurement)
    
    doc_file = procurement.file
    logger.info(doc_file)
    
    files = {'file': doc_file.open()}
    file_name = str(files['file']).split('/')[-1]
    logger.info(file_name)
    
    full_url = f'{media_host_url}{file_name}'
    logger.info(full_url)
    
    # response = requests.post(f"{media_host_url}/{file_name}", files=files)
    response = requests.post(full_url, files=files)
    logger.info(response)
    
    return response.status_code

@shared_task
def fetch_data_from_prozorro(procurement_id):
    prozorro_url = os.getenv('PROZORRO_URL')
    
    procurement = Procurement.objects.get(id=procurement_id)
    prozorro_id = procurement.prozorro_id
    
    url = os.path.join(prozorro_url, prozorro_id)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        prozorro_data = response.json()['data']
        # logger.info(prozorro_data)
        
        return True
    else:
        logger.error(response.status_code)
        return False