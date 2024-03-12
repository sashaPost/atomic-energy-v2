from django.db import models
from datetime import datetime



# Create your models here.
class NewsList(models.Model):
    # updated = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()
    source_url_ua = models.URLField(default=False)
    source_url_eng = models.URLField(default=False)
    parsed_ua = models.BooleanField(default=False)
    parsed_eng = models.BooleanField(default=False)
    downloaded_ua = models.BooleanField(default=False)
    downloaded_eng = models.BooleanField(default=False)
    file_path_ua = models.CharField(max_length=255, null=True, blank=True,)
    file_path_eng = models.CharField(max_length=255, null=True, blank=True,)
    
    def save(self, *args, **kwargs):
        if not self.updated:
            self.updated = datetime.now()
        super(NewsList, self).save(*args, **kwargs)

class Novelty(models.Model):
    novelty_url_ua = models.URLField(default=False)
    novelty_url_eng = models.URLField(default=False)
    news_list_id = models.ForeignKey(NewsList, on_delete=models.CASCADE, related_name='novelty')
    parsed_ua = models.BooleanField(default=False)
    parsed_eng = models.BooleanField(default=False)
    downloaded_ua = models.BooleanField(default=False)
    downloaded_eng = models.BooleanField(default=False)
    publication_date = models.CharField(max_length=12)
    file_path_ua = models.CharField(max_length=255, null=True, blank=True,)
    file_path_eng = models.CharField(max_length=255, null=True, blank=True,)