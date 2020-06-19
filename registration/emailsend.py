import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import *
from .html import *
from electonicswebservice.hashers import *
import random
import string
from random import randint
from datetime import datetime, timedelta
import jwt
from .models import *
from email_template.models import *
from electonicswebservice.admininfo import *
from os import path
import sys


def email_send_otp_html(otp):
    try:
        main_html = MainEmailLayoutModel.objects.get(title='main email tamplate')
        mail_content = EmailTemplate.objects.get(subject='email otp')
        if mail_content.content_1 is None:
            content_1 = ''
        else:
            content_1 = mail_content.content_1
        if mail_content.content_2 is None:
            content_2 = ''
        else:
            content_2 = mail_content.content_2.replace("#OTP", str(otp), 1)
        if mail_content.content_3 is None:
            content_3 = ''
        else:
            content_3 = mail_content.content_3
        if mail_content.content_4 is None:
            content_4 = ''
        else:
            content_4 = mail_content.content_4
        html = main_html.layout_html
        html = html.replace("#CONTANT1", content_1, 1)
        html = html.replace("#CONTANT2", content_2, 1)
        html = html.replace("#CONTANT3", content_3, 1)
        html = html.replace("#CONTANT4", content_4, 1)
        return html
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json


def email_send_otp_generate(user_data):
    rand_int = randint(10**(6-1), (10**6)-1)
    user_data.key = rand_int
    user_data.save()
    return rand_int


def smtp_details():
    smtpdb = SMTPDetailModel.objects.get()
    sender_email = smtpdb.smtp_email
    smtpurl = smtpdb.smtp_host
    smtpport = int(smtpdb.smtp_port)
    password = decrypt_message_rsa(smtpdb.smtp_password, private_key)
    return sender_email, smtpurl, smtpport, password


def email_send(receiver_email, email_subject, html):
    try:
        sender_email, smtpurl, smtpport, password = smtp_details()
        message = MIMEMultipart("alternative")
        message["Subject"] = email_subject
        message["From"] = sender_email
        message["To"] = receiver_email.email
        part1 = MIMEText("", "text")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpurl, smtpport, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email.email, message.as_string())
        return_json['valid'] = True
        return_json['message'] = "Mail Successfully Sent"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json
