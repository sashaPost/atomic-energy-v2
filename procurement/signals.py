from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Procurement
from .tasks import send_doc_file_to_media_host, fetch_data_from_prozorro

import logging



logger = logging.getLogger(__name__)

@receiver(post_save, sender=Procurement)
def trigger_send_file(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New {sender.__name__} record created. ID {instance.id}")
        procurement_id = str(instance.id)
        
        try:
            logger.info(f"Sending a file to the remote host.\n{sender.__name__} ID: {instance.id}, file: {instance.file}")
            send_doc_file_to_media_host.apply_async(args=(procurement_id,), countdown=3)
            logger.info(f"File was sent successfully.")
        except Exception as e:
            logger.warning(f"Error sending file. {sender.__name__} ID: {instance.id}")
               
        try:
            logger.info(f"Trying to fetch the procurement data from Prozorro API.\n{sender.__name__} ID: {instance.id}.")
            fetch_data_from_prozorro.apply_async(args=(procurement_id,), countdown=0)
        except Exception as e:
            logger.warning(f"Processing 'fetch_data_from_prozorro' failed.")
    else:
        old_instance = sender.objects.get(pk=instance.id)
        if instance.file != old_instance.file:
            try:
                logger.info(f"Sending a file to the remote host.\n{sender.__name__} ID: {instance.id}, file: {instance.file}")
                send_doc_file_to_media_host.apply_async(args=(procurement_id,), countdown=3)
                logger.info(f"File was sent successfully.")
            except Exception as e:
                logger.warning(f"Error sending file. {sender.__name__} ID: {instance.id}")
                
        
        # logger.info(f"{sender.__name__} record is being updated. ID {instance.id}")
        # procurement_id = str(instance.id)
        # try:
        #     send_doc_file_to_media_host.apply_async(args=(procurement_id,), countdown=3)
        # except Exception as e:
        #     logger.exception(f"Error sending file. {sender.__name__} ID: {instance.id}")