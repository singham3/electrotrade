from django.contrib import admin
from .models import *
# Register your models here.


class SearchAdminView(admin.ModelAdmin):
    list_display = ('id', 'search', 'created_at')


class EnquiryFormAdminView(admin.ModelAdmin):
    def enquiry_user(self, obj):
        return obj.user.username
    list_display = ('id', 'enquiry_user', 'product_name', 'product_company', 'product_series_num', 'created_at')


admin.site.register(Search, SearchAdminView)
admin.site.register(EnquiryForm, EnquiryFormAdminView)