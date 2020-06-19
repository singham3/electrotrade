from django.db import models
# Create your models here.


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=200)
    content_1 = models.TextField(max_length=65500, null=True, blank=True)
    content_2 = models.TextField(max_length=65500, null=True, blank=True)
    content_3 = models.TextField(max_length=65500, null=True, blank=True)
    content_4 = models.TextField(max_length=65500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class MainEmailLayoutModel(models.Model):
    title = models.CharField(max_length=200)
    layout_html = models.TextField(max_length=65500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
