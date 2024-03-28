from django.db import models
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.utils.text import slugify
# import datetime
# import os
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from scrappy_test.models import Novelty

# from .tasks import *
# import logging

# logger = logging.getLogger(__name__)



# from atomic_energy.settings import MEDIA_ROOT

# !!!Add 'help text'!!!
    # title = models.CharField(max_length=255, help_text='This is the title of the post.')

# !!!All the 'null=True, blank=True' allowed for development only!!!

# Create your models here.

# Don't even remember, what is that.
# Figure it out
class Category(models.Model):
    # add slug field.
    ua_cat = models.CharField(max_length=33, null=True, blank=True)
    en_cat = models.CharField(max_length=33, null=True, blank=True)
    
    def __str__(self):
        return self.ua_cat

# add correct arguments
class Post(models.Model):
    meta_title = models.CharField(max_length=255, null=True, blank=True)   # make default Null value, 'cause it missed in HTML
    meta_description = models.TextField(null=True, blank=True) # 'meta_tag'
    seo_tags = TaggableManager(blank=True)  # missing on the Novelty page; hide it at serialization stage.
    post_visibility = models.BooleanField(default=True)    
    
    # preview_image = models.ImageField(blank=True, upload_to='images/')    # fix this to put images into newly created directory (by post's id + date)
    # image_alt = models.CharField(max_length=255, blank=True)
    # image_visibility = models.BooleanField(default=True)    # didn't migrate yet
    
    home_page_visibility = models.BooleanField(default=True)
    
    pub_date = models.DateTimeField(auto_now_add=True)  # migration date for old posts
    indicated_date = models.DateTimeField(blank=True)
    
    added_by = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, null=True, blank=True)   # admin = User.objects.get(username='admin')
    
    migrated_novelty = models.BooleanField(default=False)    # change to True while parsing old posts
    novelty_id = models.ForeignKey(Novelty, on_delete=models.CASCADE, null=True, blank=True, related_name='post')
    old_date = models.DateField(null=True, blank=True)   # default=None, blank=True - remove the 'auto_now_add' in future
        
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='post')    

    # new code:
    # def __init__(self):
    #     super(Post, self).__init__(*args, **kwargs)
    #     self._original_preview_image = self.preview_image
    
    def __str__(self):
        # return f'{self.uaposthead_set.get().title_ua}'
        # return f'\nTitle: {self.ua_head.get().title_ua}\nID: {self.id}'
        # return f'\nMeta Title: {self.meta_title}\nID: {self.id}'
        return f'ID: {self.id}'
    
    class Meta:
        ordering = ['-indicated_date']
        get_latest_by = 'indicated_date'

    # new code:
    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         # This is an update, capture the original state
    #         self._original_preview_image = Post.objects.get(pk=self.pk).preview_image
    #     super(Post, self).save(*args, **kwargs)

    # def trigger_send_preview_image(self):
    #     if self._original_preview_image != self.preview_image:
    #         logger.info(f"Post preview image is being updated. Post ID: {self.id}")
    #         post_id = str(self.id)
    #         send_preview_img.apply_async(args=(post_id,), countdown=3)

class UaPostHead(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='ua_head')
    title_ua = models.CharField(max_length=255, null=True, blank=True)     # 'title_ua_content'
    slug = models.SlugField(max_length=255, null=True, blank=True) # will cause error if filled manually
    preview_text_ua = models.TextField(null=True, blank=True)
    
    preview_image = models.ImageField(blank=True, upload_to='images/')    # fix this to put images into newly created directory (by post's id + date)
    image_alt = models.CharField(max_length=255, blank=True)
        
    def __str__(self):
        return f'\nTitle: {self.title_ua}\nSlug: {self.slug}\nID: {self.id}\nPost ID: {self.post_id}'
    
class UaPostBody(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='ua_body')
    message_ua = RichTextField(null=True, blank=True)    # configure and add proper arguments - configured in 'settings'
    image = models.ImageField(upload_to='images/', null=True, blank=True)    # fix this to put images into newly created directory (by post's id + date)
    post_image_alt = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.post}'
    
    def clean_video_url(self):
        url = self.video_url
        try:
            parsed_url = URLValidator(schemes=['https']).parse(url)
            self.video_url = parsed_url.geturl()
        except:
            raise ValidationError('Invalid URL')
    
    class Meta:
        get_latest_by = 'post'

class EnPostHead(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='en_head')
    title_en = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    preview_text_eng = models.TextField(null=True, blank=True)
    
    preview_image = models.ImageField(blank=True, upload_to='images/')    # fix this to put images into newly created directory (by post's id + date)
    image_alt = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f'\nTitle: {self.title_en}\nSlug: {self.slug}\nID: {self.id}\nPost ID: {self.post_id}'

    
class EnPostBody(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='en_body')
    message_eng = RichTextField(null=True, blank=True)    # make 'blank=True'
    image = models.ImageField(upload_to='images/', null=True, blank=True)    # fix this to put images into newly created directory (by post's id + date)
    post_image_alt = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.post}'
    
    def clean_video_url(self):
        url = self.video_url
        try:
            parsed_url = URLValidator(schemes=['https']).parse(url)
            self.video_url = parsed_url.geturl()
        except:
            raise ValidationError('Invalid URL')
    
    class Meta:
        get_latest_by = 'post'

class PostAttachments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    attachment = models.FileField(upload_to='files/', null=True, blank=True)
    # file_alt = ?
    
    def __str__(self):
        return f'{self.post.id}'
    
    class Meta:
        get_latest_by = 'post'
        
