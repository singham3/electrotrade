from django.db import models
# Create your models here.


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=200)
    template_content = models.TextField(max_length=65500)
    footer_text = models.CharField(max_length=200)
    email_preference = models.CharField(max_length=200)
    status = models.BooleanField(max_length=200, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class MainEmailLayoutModel(models.Model):
    title = models.CharField(max_length=200)
    layout_html = models.TextField(max_length=65500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
