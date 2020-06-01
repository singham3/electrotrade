from django.contrib import admin
from .models import *
from electonicswebservice.admininfo import *
# Register your models here.


class EmailTemplateAdminView(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'created_at')


class MainEmailLayoutModelAdminView(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')


admin.site.register(EmailTemplate, EmailTemplateAdminView)
admin.site.register(MainEmailLayoutModel, MainEmailLayoutModelAdminView)
