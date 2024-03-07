from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from .models import Post, UaPostBody, EnPostBody
from .tasks import *

import logging  # Import the logging module

logger = logging.getLogger(__name__)  # Initialize the logger



# @receiver(post_save, sender=Post)
@receiver(pre_save, sender=Post)
# def trigger_send_media_task(sender, instance, created, **kwargs):
def trigger_send_media_task(sender, instance, **kwargs):
    logger.info(f"!!! 'trigger_send_media_task' was called !!!")
    # if created:
    if instance._state.adding:
        logger.info(f"New post created. Post ID: {instance.id}")  
        post_id = str(instance.id)
        send_media.apply_async(args=(post_id,), countdown=0)    # change to 'countdown=3' in case of 'post_save'
    else:
        # logger.info(f"{sender.__name__} preview image changed. {sender.__name__} ID: {instance.id}")
        # send_preview_image.apply_async(args=(str(instance.id),), countdown=3)
        try:
            old_instance = Post.objects.get(pk=instance.id)
            if instance.preview_image != old_instance.preview_image:
                logger.info(f"{sender.__name__} was changed")
                send_preview_image.apply_async(args=(str(instance.id),), countdown=0)
        except Post.DoesNotExist:
            logger.info(f"{sender.__name__} ID {instance.id} doesn't exist.")
                        
# @receiver(post_save, sender=UaPostBody)
# @receiver(post_save, sender=EnPostBody)
@receiver(pre_save, sender=UaPostBody)
@receiver(pre_save, sender=EnPostBody)
def trigger_send_body_images_tasks(sender, instance, **kwargs):
    logger.info(f"!!! 'trigger_send_body_images_tasks' was called !!!")
    logger.info(f"Signal triggered for {sender.__name__} ID: {instance.id}")
    model_name = sender._meta.model_name    # lovercase
    # logger.info(f"model_name: {model_name}")
    try:
        # send_body_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uapostbody' else 'EN'), countdown=3)
        old_instance = sender.objects.get(pk=instance.id)
        if instance.image != old_instance.image:
            send_body_img.apply_async(args=(str(instance.id), 'UA' if model_name == 'uapostbody' else 'EN'), countdown=0)
    except sender.DoesNotExist:
        logger.error(f"{sender.__name__} ID: {instance.id} does not exist")

        