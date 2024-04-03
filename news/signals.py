from django.db.models.signals import post_save
from django.dispatch import receiver 
from .models import UaPostHead, EnPostHead, UaPostBody, EnPostBody
from .tasks import send_head_img, send_body_img

import logging  # Import the logging module

logger = logging.getLogger(__name__)  # Initialize the logger



@receiver(post_save, sender=UaPostHead)
@receiver(post_save, sender=EnPostHead)
def trigger_send_head_image_task(sender, instance, created, **kwargs):
    logger.info(f"!!! 'trigger_send_preview_images_tasks' was called !!!")
    logger.info(f"Signal triggered for {sender.__name__} ID: {instance.id}")
    model_name = sender._meta.model_name    # lovercase
    
    
    
    if created:
        logger.info(f"New {sender.__name__} created. ID: {instance.id}")
        send_head_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uaposthead' else 'EN'), countdown=5)
    else:
        logger.info(f"* 'else' block was triggered *")
        try:
            send_head_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uaposthead' else 'EN'), countdown=5)
            
            # old_instance = sender.objects.get(pk=instance.id)
            # old_image_filename = old_instance.preview_image.name
            # logger.info(f"'old_image_filename': {old_image_filename}")
            # logger.info(f"'upd_image_filename': {instance.preview_image.name}")
            # if instance.preview_image.name != old_image_filename:
            #     logger.info(f"* image file was changed *")
            #     send_head_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uaposthead' else 'EN'), countdown=5)
        except sender.DoesNotExist:
            logger.error(f"{sender.__name__} ID: {instance.id} does not exist")
    
@receiver(post_save, sender=UaPostBody)
@receiver(post_save, sender=EnPostBody)
def trigger_send_body_image_task(sender, instance, created, **kwargs):
    logger.info(f"!!! 'trigger_send_body_images_tasks' was called !!!")
    logger.info(f"Signal triggered for {sender.__name__} ID: {instance.id}")
    model_name = sender._meta.model_name    # lovercase
    if created:
        logger.info(f"New {sender.__name__} created. ID: {instance.id}")
        send_body_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uapostbody' else 'EN'), countdown=5)
    else:
        logger.info(f"* 'else' block was triggered *")
        try:
            send_body_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uapostbody' else 'EN'), countdown=5)
        except sender.DoesNotExist:
            logger.error(f"{sender.__name__} ID: {instance.id} does not exist")

        