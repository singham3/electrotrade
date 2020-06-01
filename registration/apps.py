from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from datetime import datetime
from random import randint
from os import path
from electonicswebservice.hashers import *
import json


class RegistrationConfig(AppConfig):
    name = 'registration'


user_json_data = eval(open("/var/www/html/electonicswebservice/config/adminappconfig/config.json", "r").read())


def create_smtp_details(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from .models import SMTPDetailModel
    try:
        SMTPDetailModel.objects.get()
    except SMTPDetailModel.DoesNotExist:
        if not path.exists('config/adminappconfig/private_key.pem') or not path.exists('config/adminappconfig/public_key.pem'):
            exprivatekey, expublickey = generate_keys_rsa()
            open('config/adminappconfig/private_key.pem', 'wb').write(exprivatekey.encode())
            open('config/adminappconfig/public_key.pem', 'wb').write(expublickey.encode())
            public_key = open('config/adminappconfig/public_key.pem', 'rb').read().decode()
        else:
            public_key = open('config/adminappconfig/public_key.pem', 'rb').read().decode()
        SMTPDetailModel.objects.create(smtp_host=user_json_data['smtp_details']['SMTPUSERNAME'],
                                       smtp_email=user_json_data['smtp_details']['SMTP_EMAIL'],
                                       smtp_password=encrypt_message_rsa(user_json_data['smtp_details']['SMTPPASSWORD'],
                                                                         public_key),
                                       smtp_port=user_json_data['smtp_details']['SMTPPORT']
                                       )
        user_json_data['smtp_details']['SMTPPASSWORD'] = encrypt_message_rsa(
                                                                        user_json_data['smtp_details']['SMTPPASSWORD'],
                                                                        public_key)
        json.dump(user_json_data, open("config/adminappconfig/config.json", "w"), indent=2)


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_smtp_details)
