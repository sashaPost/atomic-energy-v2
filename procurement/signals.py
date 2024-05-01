from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import requests
from .models import Procurement
# from .search_indexes import update_index
from .tasks import (
    send_doc_file_to_media_host, 
    fetch_data_from_prozorro,
    # update_procurement_index,
)
import logging


logger = logging.getLogger(__name__)


#
# @receiver(post_save, sender=Procurement)
# @receiver(post_delete, sender=Procurement)
# def update_index_on_procurement_change(sender, instance, **kwargs):
#     logger.info(f"* 'update_index_on_procurement_change' signal was sent *")
#     update_procurement_index()


@receiver(post_save, sender=Procurement)
# def trigger_send_file(sender, instance, created, **kwargs):
def process_new_procurement_record(sender, instance, created, **kwargs):
    logger.info(f"* 'process_new_procurement_record' signal was triggered *")
    prozorro_id = str(instance.prozorro_id)
    if created:
        logger.info(f"New {sender.__name__} record created. ID {instance.id}")
        
        logger.info(f"File: {instance.file}\nFile type: {type(instance.file)}")
        # logger.info(f"* File: {instance.file}\nFile type: {type(str(instance.file))} *")
        
        try:
            logger.info(f"Sending a file to the remote host.\n{sender.__name__} ID: {instance.id}, file: {instance.file}")
            # send_doc_file_to_media_host.apply_async(args=(instance,), countdown=3)
            send_doc_file_to_media_host.apply_async(args=(instance.id,), countdown=3)
            logger.info(f"File was sent successfully.")
        # except Exception as e:
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Error sending file. {sender.__name__}\n\
                    ID: {instance.id}\n\
                        Error: {e}"
            )
                
               
        try:
            logger.info(f"Trying to fetch the procurement data from Prozorro API.\n{sender.__name__} ID: {instance.id}.")
            # fetch_data_from_prozorro.apply_async(args=(instance,), countdown=3)
            fetch_data_from_prozorro.apply_async(args=(prozorro_id, instance.id), countdown=3)
            
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Processing 'fetch_data_from_prozorro' failed.\n\
                    Error: {e}"
            )
    else:
        try:
            send_doc_file_to_media_host.apply_async(args=(instance.id,), countdown=3)
            fetch_data_from_prozorro.apply_async(args=(prozorro_id, instance.id), countdown=3)
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Error: {e}"
            )
        # old_instance = sender.objects.get(pk=instance.id)
        # if instance.file != old_instance.file:
        #     try:
        #         logger.info(f"Sending a file to the remote host.\n{sender.__name__} ID: {instance.id}, file: {instance.file}")
        #         send_doc_file_to_media_host.apply_async(args=(prozorro_id,), countdown=3)
        #         logger.info(f"File was sent successfully.")
        #     except Exception as e:
        #         logger.warning(f"Error sending file. {sender.__name__} ID: {instance.id}")
                
        
        # logger.info(f"{sender.__name__} record is being updated. ID {instance.id}")
        # prozorro_id = str(instance.id)
        # try:
        #     send_doc_file_to_media_host.apply_async(args=(prozorro_id,), countdown=3)
        # except Exception as e:
        #     logger.exception(f"Error sending file. {sender.__name__} ID: {instance.id}")