from django.utils.translation import ugettext
import logging
import json
from django.forms.models import model_to_dict
from os import path
from .hashers import *
from django.core.paginator import Paginator


token_key = json.load(open('/var/www/html/electonicswebservice/config/secret-key.json'))
jsondata = json.load(open("/var/www/html/electonicswebservice/config/adminappconfig/config.json"))
private_config_data = json.load(open('/var/www/html/electonicswebservice/config/adminappconfig/project_config.json'))


logging.basicConfig(filename="/var/www/html/electonicswebservice/debug/debug.log",
                    format='%(asctime)s %(name)-15s %(levelname)-5s %(message)s : [%(pathname)s line %(lineno)d, in %(funcName)s ]',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

return_json = {
                "valid": False,
                "message": "",
                "count_result": 0,
                "data": None
            }

if path.exists('/var/www/html/electonicswebservice/config/adminappconfig/private_key.pem') and path.exists('/var/www/html/electonicswebservice/config/adminappconfig/public_key.pem'):
    private_key = open('/var/www/html/electonicswebservice/config/adminappconfig/private_key.pem', 'rb').read().decode()
    public_key = open('/var/www/html/electonicswebservice/config/adminappconfig/public_key.pem', 'rb').read().decode()
else:
    exprivatekey, expublickey = generate_keys_rsa()
    open('/var/www/html/electonicswebservice/config/adminappconfig/private_key.pem', 'wb').write(exprivatekey.encode())
    open('/var/www/html/electonicswebservice/config/adminappconfig/public_key.pem', 'wb').write(expublickey.encode())
    private_key = open('/var/www/html/electonicswebservice/config/adminappconfig/private_key.pem', 'rb').read().decode()
    public_key = open('/var/www/html/electonicswebservice/config/adminappconfig/public_key.pem', 'rb').read().decode()


def UserInfo(user_data):
    json_user_data = model_to_dict(user_data)
    json_user_data.pop('password')
    if 'last_login' in json_user_data:
        json_user_data.pop('last_login')
    if 'updated_at' in json_user_data:
        json_user_data.pop('updated_at')
    json_user_data.pop('key')
    if user_data.user_profile_img:
        json_user_data['user_profile_img'] = user_data.user_profile_img.url
    else:
        json_user_data['user_profile_img'] = ''
    if user_data.varification_document_front:
        json_user_data['varification_document_front'] = user_data.varification_document_front.url
    else:
        json_user_data['varification_document_front'] = ''
    if user_data.varification_document_back:
        json_user_data['varification_document_back'] = user_data.varification_document_back.name
    else:
        json_user_data['varification_document_back'] = ''
    if user_data.city:
        json_user_data['city'] = str(user_data.city.id)
    if user_data.state:
        json_user_data['state'] = str(user_data.state.id)
    if user_data.gender:
        json_user_data['gender'] = str(user_data.gender.id)
    if user_data.role:
        json_user_data['role'] = str(user_data.role.id)

    if user_data.business_type:
        json_user_data['business_type'] = str(user_data.business_type.id)
    if user_data.document_type:
        json_user_data['document_type'] = str(user_data.document_type.id)
    for i in json_user_data:
        if json_user_data[i] is None:
            json_user_data[i] = ''
    return json_user_data


def alldata(model, page):
    try:
        all_model_data = model.objects.all()
        paginator = Paginator(all_model_data, 10)
        contacts = paginator.get_page(page)
        return contacts, None
    except Exception as e:
        return None, e


def city_json_data(obj):
    city_json_data_list = []
    for i in obj:
        j = model_to_dict(i)
        j.pop('state_id')
        if i.city_image:
            j['city_image'] = i.city_image.url
        else:
            j['city_image'] = ""
        city_json_data_list.append(j)
    if any(city_json_data_list):
        return city_json_data_list
    else:
        return ""


def state_json_data(obj):
    state_json_data_list = []
    for i in obj:
        j = model_to_dict(i)
        state_json_data_list.append(j)
    if any(state_json_data_list):
        return state_json_data_list
    else:
        return ""


def business_type_json_data(obj):
    business_type_json_data_list = []
    for i in obj:
        j = model_to_dict(i)
        business_type_json_data_list.append(j)
    if any(business_type_json_data_list):
        return business_type_json_data_list
    else:
        return ""
