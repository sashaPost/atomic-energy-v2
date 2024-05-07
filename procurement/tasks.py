from celery import shared_task
import requests
import os
from dotenv import load_dotenv
from django.db import IntegrityError
from .models import (
    Procurement, 
    ProcuringEntity,
    Value,
    Item,
    TenderPeriod,
    TenderStep,
)
# from .search_indexes import update_index
import logging



load_dotenv('.env')

logger = logging.getLogger(__name__)


# @shared_task
# def update_procurement_index():
#     logger.info(f"* 'update_procurement_index' was triggered *")
#     update_index()
    

@shared_task
def send_doc_file_to_media_host(instance_id):
    """
    Uploads a file associated with a Procurement instance to a media host.

    Args:
        instance_id: The ID of the Procurement instance that has the file.

    Returns:
        The HTTP status code of the upload request if successful, 
        False otherwise.
    """
    logger.info(f"* 'send_doc_file_to_media_host' was task triggered *")
    MEDIA_HOST_URL = os.getenv('MEDIA_HOST_FILES_URL')    
    API_KEY = os.getenv('API_KEY')  
    logger.info(f"'MEDIA_HOST_URL': {MEDIA_HOST_URL}")
    
    procurement = Procurement.objects.get(id=instance_id)
    logger.info(f"'procurement': {procurement}")
    
    doc_file = procurement.file
    logger.info(f"'doc_file': {doc_file}")
        
    files = {'file': doc_file.open()}
    file_name = str(files['file']).split('/')[-1]
    logger.info(f"'file_name': {file_name}")
    
    full_url = f'{MEDIA_HOST_URL}{file_name}'
    logger.info(f"Request URL: {full_url}")
    
    headers = {'Authorization': f'{API_KEY}'}
    
    try:
        response = requests.post(full_url, files=files, headers=headers)
        logger.info(response)       
        if response.status_code == 200:
            logger.info(f"File was successfully sent!") 
            return response.status_code
        else:
            logger.info(f"File wasn't sent. Status Code: {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Something went wrong processing \
            'send_doc_file_to_media_host'")
        logger.warning(f"Exception: {e}")
        return False


# !!! curl https://public-api.prozorro.gov.ua/api/2.5/tenders/42150eeee5174bffb09484f02eecf385 | jq
# Procurement.prozorro_id => 42150eeee5174bffb09484f02eecf385
def update_model_field(instance, field_name, new_value):
    """
    Updates the specified field of a model instance and saves it.

    Args:
        instance: The model instance to update.
        field_name: The name of the field to update.
        new_value: The new value for the field.
    """
    logger.info(f"* 'update_model_field' was triggerred *")
    logger.info(f"Istance ID: {instance.id}\nfield_name: {field_name}\nnew_value: {new_value}")
    setattr(instance, field_name, new_value)
    instance.save()

def get_values(instance, request_data, defaults_dict):
    """
    Extracts nested values from a dictionary and updates a model instance.

    Args:
        instance: The model instance to update.
        request_data: The dictionary containing the nested values.
        defaults_dict: A dictionary mapping field names to key chains.
    """
    logger.info(f"* 'get_values' was triggerred *")
    
    for key in defaults_dict.keys():
        desired_data = request_data
        logger.info(f"'defaults_dict' 'key': {key}")
        
        for item in defaults_dict[key]:
            logger.info(f"'item': {item}")
            desired_data = desired_data.get(item, None)
            if isinstance(desired_data, list):
                desired_data = desired_data[0]
            
            logger.info(f"'desired_data' for '{item}': {desired_data}")
            if item is defaults_dict[key][-1]:
                logger.info(f"Last 'item' of the keychain ('desired_data'): {desired_data}")
                update_model_field(instance, key, desired_data)
                
def process_procuring_entity(
    procurement,
    request_data,
):
    """
    Processes ProcuringEntity data from Prozorro and saves it to the database.

    Args:
        procurement: The Procurement object to associate the entity with.
        request_data: The Prozorro response data.

    Returns:
        The created or updated ProcuringEntity instance.
    """
    logger.info(f"* 'process_procuring_entity' was triggerred *")
    defaults_dict={
        'identifier_id': ['procuringEntity', 'identifier', 'id'],
        'identifier_scheme': ['procuringEntity', 'identifier', 'scheme'],
        'identifier_name': ['procuringEntity', 'identifier', 'legalName'],
        'country_name': ['procuringEntity', 'address', 'countryName'],
        'postal_code': ['procuringEntity', 'address', 'postalCode'],    # !!! MAY BE MISSED IN RESPONSE
        'region': ['procuringEntity', 'address', 'region'],
        'locality': ['procuringEntity', 'address', 'locality'],
        'address': ['procuringEntity', 'address', 'streetAddress'],    # !!! MAY BE MISSED IN RESPONSE
        'contact_email': ['procuringEntity', 'contactPoint', 'email'],
        'contact_phone': ['procuringEntity', 'contactPoint', 'telephone'],
        'contact_url': ['procuringEntity', 'contactPoint', 'url'],
        'contact_name': ['procuringEntity', 'contactPoint', 'name'],
    }
    procuring_entity, _ = ProcuringEntity.objects.get_or_create(procurement=procurement) 
    get_values(procuring_entity, request_data, defaults_dict)
    return procuring_entity
    
def process_item(
    procurement,
    request_data,
):
    """
    Processes and saves Item data extracted from the Prozorro response.

    Args:
        procurement: The Procurement object associated with the Item.
        request_data: The Prozorro response data.
    """
    logger.info(f"* 'process_item' was triggerred *")
    defaults_dict = {
        'description': ['items', 'description'],
        'classification_id': ['items', 'classification', 'id'],
        'classification_scheme': ['items', 'classification', 'scheme'],
        'classification_description': ['items', 'classification', 'description'],
        'quantity': ['items', 'quantity'],
        'unit_name': ['items', 'unit', 'name'],
        'delivery_date': ['items', 'deliveryDate', 'endDate']
    }
    item_obj, _ = Item.objects.get_or_create(procurement=procurement)
    get_values(item_obj, request_data, defaults_dict)
    return item_obj

def process_value(
    procurement,
    request_data,
):
    """
    Processes and saves Value data extracted from the Prozorro response.

    Args:
        procurement: The Procurement object associated with the Value.
        request_data: The Prozorro response data.
    """
    logger.info(f"* 'process_value' was triggerred *")
    defaults_dict={
        'amount': ['value', 'amount'],
        'currency': ['value', 'currency'],
    }
    value_obj, _ = Value.objects.get_or_create(procurement=procurement)
    get_values(value_obj, request_data, defaults_dict)
    return value_obj

def process_tender_step(
    procurement,
    request_data,
):
    """
    Processes and saves TenderStep data extracted from the Prozorro response.

    Args:
        procurement: The Procurement object associated with the TenderStep.
        request_data: The Prozorro response data.
    """
    logger.info(f"* 'process_tender_step' was triggerred *")
    defaults_dict={
        'currency': ['minimalStep', 'currency'],
        'amount': ['minimalStep', 'amount'],
    }
    tender_step_obj, _ = TenderStep.objects.get_or_create(procurement=procurement)
    get_values(tender_step_obj, request_data, defaults_dict)
    return tender_step_obj

def process_tender_period(
    procurement,
    request_data,
):
    """
    Processes and saves TenderPeriod data extracted from the Prozorro response.

    Args:
        procurement: The Procurement object associated with the TenderPeriod.
        request_data: The Prozorro response data.
    """
    logger.info(f"* 'process_tender_period' was triggerred *")
    defaults_dict={
        'start_date': ['tenderPeriod', 'startDate'],
        'end_date': ['tenderPeriod', 'endDate'],
    }
    tender_period_obj, _ = TenderPeriod.objects.get_or_create(procurement=procurement)
    get_values(tender_period_obj, request_data, defaults_dict)
    return tender_period_obj


@shared_task
def fetch_data_from_prozorro(prozorro_id, instance_id):
    """
    Fetches data from Prozorro and saves it to the associated Procurement model.

    Args:
        prozorro_id: The ID of the tender on Prozorro.
        instance_id: The ID of the Procurement object in your database.
    """
    logger.info(f"* 'fetch_data_from_prozorro' was triggered *")
    
    PROZORRO_URL = os.getenv('PROZORRO_URL')
    logger.info(f"'PROZORRO_URL': {PROZORRO_URL}")
    
    procurement = Procurement.objects.get(id=instance_id)
    logger.info(f"'Procurement being processed: {procurement}")
    
    # prozorro_id = procurement.prozorro_id
    logger.info(f"'Prozorro ID': {prozorro_id}")
    
    url = os.path.join(PROZORRO_URL, prozorro_id)
    logger.info(f"'URL': {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        # create helper functions to store the data in the database
        logger.info(f"Request was successful!")
        prozorro_data = response.json()['data']
        
        # logger.info(f"'procuringEntity': {prozorro_data['procuringEntity']}")
        # logger.info(f"'procuringEntity->name': {prozorro_data['procuringEntity']['name']}")
        
        # logger.info(f"'value': {prozorro_data['value']}")
        
        # logger.info(f"'items': {prozorro_data['items']}")
        
        # logger.info(f"'tenderPeriod': {prozorro_data['tenderPeriod']}")
        
        # logger.info(f"'TenderStep': {prozorro_data['value']}")
        # logger.info(f"'TenderStep.currency': {prozorro_data['value']['currency']}")
        # logger.info(f"'TenderStep.amount': {prozorro_data['value']['amount']}")
        
        try:
            # Fetch or create main 'Procurement' record:
            procurement, _ = Procurement.objects.get_or_create(id=instance_id)
            
            # ProcuringEntity:
            procuring_entity = process_procuring_entity(
                procurement=procurement,
                request_data=prozorro_data,
            )
            
            # Value:
            value_obj = process_value(
                procurement=procurement,
                request_data=prozorro_data,
            )
            
            # Item:
            item_obj = process_item(
                procurement=procurement,
                request_data=prozorro_data,
            )
            
            # TenderPeriod:
            tender_period = process_tender_period(
                procurement=procurement,
                request_data=prozorro_data,
            )
            
            # TenderStep:
            tender_step = process_tender_step(
                procurement=procurement,
                request_data=prozorro_data,
            )
            
            logger.info(f"'Procurement': {procurement}")
            # logger.info(f"'ProcuringEntity': {procuring_entity}")
            
            return True
        except (ValueError, KeyError, IntegrityError) as e:
            logger.error(f"Error processing Prozorro data for procurement {instance_id}: {e}")
            return False
    else:
        logger.error(response.status_code)
        return False