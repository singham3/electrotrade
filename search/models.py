from django.db import models
from registration.models import *


class Search(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.PROTECT, null=True, blank=True)
    search = models.CharField(max_length=250, null=True, blank=True)
    search_count = models.IntegerField(default=0)
    search_result_status = models.BooleanField(default=False)
    search_result_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class EnquiryForm(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    product_name = models.CharField(max_length=250)
    product_company = models.CharField(max_length=250)
    product_series_num = models.CharField(max_length=200, null=True, blank=True)
    prod_description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)