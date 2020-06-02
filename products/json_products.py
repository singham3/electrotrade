from django.forms.models import model_to_dict
from electonicswebservice.admininfo import *
from registration.models import *
import json


def brand_data_json(i):
    j = model_to_dict(i)
    if i.logo:
        j['logo'] = i.logo.url
    else:
        j['image_slave_one'] = ''
    return j


def product_data_json(i):
    j = model_to_dict(i)
    if i.category:
        j['category'] = str(i.category.id)
    elif i.category is None:
        j['category'] = ""
    if i.brand:
        j['brand'] = brand_data_json(i.brand)
    elif i.brand is None:
        j['brand'] = ""
    if i.image:
        j['image'] = i.image.url
    else:
        j['image'] = ''
    if i.in_offer is None:
        j['in_offer'] = ""
    if i.image_slave_one:
        j['image_slave_one'] = i.image_slave_one.url
    else:
        j['image_slave_one'] = ''
    if i.image_slave_two:
        j['image_slave_two'] = i.image_slave_two.url
    else:
        j['image_slave_two'] = ''
    if i.image_slave_three:
        j['image_slave_three'] = i.image_slave_three.url
    else:
        j['image_slave_three'] = ''
    if i.image_slave_four:
        j['image_slave_four'] = i.image_slave_four.url
    else:
        j['image_slave_four'] = ''
    if i.gst_per is None:
        j['gst_per'] = 0.0
    if i.delivery_charges is None:
        j['delivery_charges'] = 0.0
    return j


def order_address_data_json(i):
    order_dict = {}
    order_dict['address'] = []
    for j in i:
        k = model_to_dict(j)
        if j.user:
            k['user'] = str(j.user.id)
        if j.city:
            k['city'] = str(j.city.id)
        if j.state:
            k['state'] = str(j.state.id)
        for m in k:
            if k[m] is None:
                k[m] = ""
        order_dict['address'].append(k)
    order_dict['cities'] = city_json_data(City.objects.all())
    order_dict['states'] = state_json_data(State.objects.all())
    return order_dict


def product_payments_json(obj):
    k = model_to_dict(obj)
    if obj.user:
        k['user'] = str(obj.user.id)
    if obj.order:
        k['order'] = str(obj.order.order_id)
    if obj.reward:
        k['reward'] = obj.reward.reward_point
    if obj.payment_method:
        k['payment_method'] = obj.payment_method.method
    for m in k:
        if k[m] is None:
            k[m] = ""
    return k


def product_reward_json(obj):
    k = model_to_dict(obj)
    if obj.user:
        k['user'] = str(obj.user.id)
    for m in k:
        if k[m] is None:
            k[m] = ""
    return k


def product_spec_json(obj):
    try:
        product_spec_list = []
        for spec in obj:
            jspec = model_to_dict(spec)
            if spec.product:
                jspec['product'] = str(spec.product.id)
            if spec.description:
                jspec['description'] = eval(spec.description)
            if spec.second_description:
                jspec['second_description'] = eval(spec.second_description)
            if spec.third_description:
                jspec['third_description'] = eval(spec.third_description)
            for l in jspec:
                if jspec[l] is None:
                    jspec[l] = ''
            product_spec_list.append(jspec)
        return product_spec_list
    except Exception as e:
        error = []
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error.append(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return error