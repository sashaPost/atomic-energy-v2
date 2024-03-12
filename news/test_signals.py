from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver 
from .models import Post
from .tasks import *

import logging  # Import the logging module

logger = logging.getLogger(__name__)  # Initialize the logger



@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, **kwargs):
    try:
        instance._pre_save_state = sender.objects.get(pk=instance.id)
    except sender.DoesNotExist:
        instance._pre_save_state = None

@receiver(post_save, sender=Post)
def trigger_send_media_task(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New post created. Post ID: {instance.id}")  
        post_id = str(instance.id)
        send_media.apply_async(args=(post_id,), countdown=3)
    elif instance._pre_save_state and instance._pre_save_state.preview_image != instance.preview_image:
        logger.info(f"Post preview image is being updated. Post ID: {instance.id}")
        post_id = str(instance.id)
        send_preview_img.apply_async(args=(post_id,), countdown=3)

    # else:
    #     logger.info(f"Post being updated. Post ID: {instance.id}")

    #     # update_fields = instance.get_deferred_fields()
    #     pre_save_instance = getattr(instance, '_pre_save_instance', None)

    #     if pre_save_instance:
    #         if pre_save_instance.preview_image != instance.preview_image:
    #             logger.info(f"Post preview image is being updated. Post ID: {instance.id}")
    #             post_id = str(instance.id)
    #             send_preview_img.apply_async(args=(post_id,), countdown=3)


    #     # if 'preview_image' in update_fields:
    #     #     logger.info(f"Post preview image is being updated.\nPost ID: {instance.id}")
    #     #     post_id = str(instance.id)
    #     #     send_preview_img.apply_async(args=(post_id,), countdown=3)
        
    #     ua_post_bodies = instance.ua_body.all()
    #     for body in ua_post_bodies:
    #         if 'image' in update_fields:
    #             logger.info(f"UaPostBody image is being updated.\nUaPostBody ID: {body.id}")
    #             ua_body_id = str(body.id)
    #             send_body_img.apply_async(args=(ua_body_id, 'UA'), countdown=3)
        
    #     en_post_bodies = instance.en_body.all()
    #     for body in en_post_bodies:
    #         if 'image' in update_fields:
    #             logger.info(f"EnPostBody image is being updated.\nEnPostBody ID: {body.id}")
    #             en_body_id = str(body.id)
    #             send_body_img.apply_async(args=(en_body_id, 'EN'), countdown=3)
