import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import *
from .html import *
from electonicswebservice.hashers import *
import random
import string
from datetime import datetime, timedelta
import jwt
from .models import *
from email_template.models import *
from electonicswebservice.admininfo import *
from os import path
import sys


token_key = json.load(open('/var/www/html/electonicswebservice/config/secret-key.json'))
jsondata = json.load(open("/var/www/html/electonicswebservice/config/adminappconfig/config.json"))
private_config_data = json.load(open('/var/www/html/electonicswebservice/config/adminappconfig/project_config.json'))


def generate_url(user_obj):
    key = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    user_obj.key = key
    user_obj.save()
    userdat = [user_obj.email, user_obj.username, user_obj.account_id, key]
    token = "{}".format(jwt.encode(
                                {"data": encrypt_message_rsa(str(userdat), public_key),
                                 'token_created_at': str(datetime.now()),
                                 'a': {2: True},
                                 'exp': datetime.utcnow() + timedelta(seconds=86400)},
                                token_key["token_key"], algorithm='HS256').decode('utf-8'))
    return '''http://{}:{}/api/v1/user/forgot-password/referral/?token={}'''.format(private_config_data['host'],
                                                                                    private_config_data['port'], token)


def email_html(email_content, email_template_data):
    try:
        maincontaint = str(email_template_data.template_content)
        maincontaint = maincontaint.replace('##USERNAME##', email_content['username'], 1)
        maincontaint = maincontaint.replace('##RESETURL##', email_content['rmpurl'], 1)
        maincontaint = maincontaint.replace('##SYSTEM_APPLICATION_NAME##', email_content['fromname'], 1)
        maincontaint = maincontaint.replace('##SYSTEM_LOGO##', '', 1)
        footer = str(email_template_data.footer_text)
        footer = footer.replace('##YEAR##', str(datetime.now().year), 1)
        mainemaillayoyt = MainEmailLayoutModel.objects.get()
        html = str(mainemaillayoyt.layout_html)
        html = html.replace("##EMAIL_CONTENT##", maincontaint, 1)
        html = html.replace("##EMAIL_FOOTER##", "", 1)
        html = html.replace("##COPYRIGHT_TEXT##", footer, 1)
        return html
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        print(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return None


def smtp_details():
    if SMTPDetailModel.objects.filter().exists():
        smtpdb = SMTPDetailModel.objects.get()
        sender_email = smtpdb.smtp_email
        smtpurl = smtpdb.smtp_host
        smtpport = int(smtpdb.smtp_port)
        password = decrypt_message_rsa(smtpdb.smtp_password, private_key)
    else:
        sender_email = jsondata['smtp_details']["SMTP_EMAIL"]
        smtpurl = jsondata['smtp_details']["SMTPUSERNAME"]
        smtpport = int(jsondata['smtp_details']["SMTPPORT"])
        password = decrypt_message_rsa(jsondata['smtp_details']["SMTPPASSWORD"], private_key)
    return sender_email, smtpurl, smtpport, password


def email_send(receiver_email, email_template_data):
    try:
        sender_email, smtpurl, smtpport, password = smtp_details()
        message = MIMEMultipart("alternative")
        message["Subject"] = email_template_data.subject
        message["From"] = sender_email
        message["To"] = receiver_email.email
        email_content = {"username": receiver_email.username, "rmpurl": generate_url(receiver_email),
                         "fromname": "Admin LTE"}
        html = email_html(email_content, email_template_data)
        part1 = MIMEText("", "text")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpurl, smtpport, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email.email, message.as_string())
        return {"msg": "Mail Successfully Sent"}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return {"error": str((e, exc_type, f_name, exc_tb.tb_lineno))}
