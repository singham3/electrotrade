from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket


class AdminConfig(AppConfig):
    name = 'Admin_user'


user_json_data = eval(open("/var/www/html/electonicswebservice/config/adminappconfig/config.json", "r").read())['Register']


def create_test_user(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    user = get_user_model()
    manager = user.objects
    try:
        manager.get(username="admin")
    except user.DoesNotExist:
        manager.create_superuser(username=user_json_data['username'], email=user_json_data['email'],
                                 first_name=user_json_data['first_name'], last_name=user_json_data['last_name'],
                                 is_superuser=True, is_staff=True, is_active=True, mobile=user_json_data['mobile'],
                                 date_of_birth=datetime.strptime(user_json_data['date_of_birth'], '%m/%d/%Y'),
                                 admin_img=user_json_data['user_profile_img'], account_id=randint(10**(8-1), (10**8)-1),
                                 password=user_json_data['password'])


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)
