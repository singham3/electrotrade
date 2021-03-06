from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import decorator_from_middleware
from random import randint
from .middleware import *
from .services import *
from django.contrib import auth
import jwt
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict
from django.core.paginator import Paginator
from .emailsend import *
import os
import sys
import hashlib
from products.models import UserCategory, Category, OrderAddress
from django.db.models.query import QuerySet
from electonicswebservice.admininfo import *
import html


@api_view(['GET', 'POST'])
@decorator_from_middleware(UserRegisterMiddleware)
def user_register(request, form=None):
    if request.method == "POST":
        try:
            new_user = CreateUserService.execute({
                'password': form.cleaned_data.get('password'),
                'username': form.cleaned_data.get('username'),
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'email': form.cleaned_data.get('email'),
                'gender': form.cleaned_data.get('gender').id if form.cleaned_data.get('gender') else None,
                'role': form.cleaned_data.get('role').id if form.cleaned_data.get('role') else None,
                'is_active': form.cleaned_data.get('is_active'),
                'mobile': form.cleaned_data.get('mobile'),
                'date_of_birth': form.cleaned_data.get('date_of_birth'),
                'account_id': form.cleaned_data.get('account_id'),
                'city': form.cleaned_data.get('city').id if form.cleaned_data.get('city') else None,
                'state': form.cleaned_data.get('state').id if form.cleaned_data.get('state') else None,
                'address': form.cleaned_data.get('address'),
                'pincode': form.cleaned_data.get('pincode'),
                'gst_number': form.cleaned_data.get('gst_number'),
                'document_type': form.cleaned_data.get('document_type').id if form.cleaned_data.get(
                    'document_type') else None,
                'business_type': form.cleaned_data.get('business_type').id if form.cleaned_data.get(
                    'business_type') else None,
                'business_name': form.cleaned_data.get('business_name'),
                'business_description': form.cleaned_data.get('business_description'),
                'alternate_mobile': form.cleaned_data.get('alternate_mobile'),
                'status': True if form.cleaned_data.get('status') else None,
            }, {'user_profile_img': form.cleaned_data.get('user_profile_img'),
                'varification_document_front': form.cleaned_data.get('varification_document_front'),
                'varification_document_back': form.cleaned_data.get('varification_document_back'),
                })
            if isinstance(new_user, dict):
                return_json['valid'] = True
                return_json['message'] = "Error to Created user "
                return_json['count_result'] = 1
                return_json['data'] = new_user
            else:
                return_json['valid'] = True
                return_json['message'] = "User Successfully Created"
                return_json['count_result'] = 1
                return_json['data'] = UserInfo(new_user)
            return JsonResponse(return_json, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return_json['valid'] = False
            return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
            return_json['count_result'] = 1
            return_json['data'] = None
            return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
@decorator_from_middleware(LoginMiddleware)
def user_login(request, form):
    if request.method == "POST":
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if Register.objects.filter(username=username).exists():
                try:
                    user_data = Register.objects.get(username=username,
                                                     password=hashlib.sha256(password.encode()).hexdigest())
                    if user_data is not None:

                        token = jwt.encode({
                            'account_id': user_data.account_id,
                            'username': user_data.username,
                            'token_created_at': str(datetime.now()),
                            'a': {2: True}},
                            token_key["token_key"],
                            algorithm='HS256'
                        )
                        user_data.token = token.decode()
                        user_data.last_login = datetime.now()
                        user_data.key = None
                        user_data.save()
                        users_data = UserInfo(user_data)
                        u_data = Register.objects.get(username=username,
                                                      password=hashlib.sha256(password.encode()).hexdigest())
                        if UserCategory.objects.filter(user=u_data).exists():
                            category_data = UserCategory.objects.get(user=u_data)
                            users_data['Category'] = category_data.list_category
                        else:
                            users_data['Category'] = [""]
                        return_json['valid'] = True
                        return_json['message'] = "Successfully Login"
                        return_json['count_result'] = 1
                        return_json['data'] = users_data

                        return JsonResponse(return_json, safe=False, status=200)
                    else:
                        return_json['valid'] = False
                        return_json['message'] = "Incorrect username and password"
                        return_json['count_result'] = 1
                        return_json['data'] = None
                        return JsonResponse(return_json, status=200, safe=False)
                except Register.DoesNotExist:
                    return_json['valid'] = False
                    return_json['message'] = "Invalid Username and Password"
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    return JsonResponse(return_json, status=200, safe=False)
            else:
                return_json['valid'] = False
                return_json['message'] = "Invalid Username and Password"
                return_json['count_result'] = 1
                return_json['data'] = None
                return JsonResponse(return_json, status=200, safe=False)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return_json['valid'] = False
            return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
            return_json['count_result'] = 1
            return_json['data'] = None
            return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ProfileMiddleware)
def user_profile(request, form=None):
    try:
        if request.method == "POST":
            user_data = Register.objects.get(account_id=request.COOKIES['id'])
            if form.cleaned_data.get('business_type'):
                user_data.business_type = BusinessType.objects.get(title=form.cleaned_data.get('business_type'))
            if form.cleaned_data.get('business_name'):
                user_data.business_name = form.cleaned_data.get('business_name')
            if form.cleaned_data.get('alternate_mobile'):
                user_data.alternate_mobile = form.cleaned_data.get('alternate_mobile')
            if form.cleaned_data.get('business_description'):
                user_data.business_description = form.cleaned_data.get('business_description')
            if form.cleaned_data.get('state'):
                user_data.state = State.objects.get(state_name=form.cleaned_data.get('state'))
            if form.cleaned_data.get('city'):
                user_data.city = City.objects.get(city_name=form.cleaned_data.get('city'))
            if form.cleaned_data.get('address'):
                user_data.address = form.cleaned_data.get('address')
            if form.cleaned_data.get('pincode'):
                user_data.pincode = form.cleaned_data.get('pincode')
            if form.cleaned_data.get('user_profile_img'):
                user_data.user_profile_img = form.cleaned_data.get('user_profile_img')
            user_data.save()
            return_json['valid'] = True
            return_json['message'] = "Successfully Update"
            return_json['count_result'] = 1
            return_json['data'] = UserInfo(Register.objects.get(account_id=request.COOKIES['id']))
            return JsonResponse(return_json, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def user_logout_view(request):
    try:
        user_data = Register.objects.get(account_id=request.COOKIES['id'])
        user_data.token = None
        user_data.key = None
        user_data.save()
        request.COOKIES.pop('id')
        return_json['valid'] = True
        return_json['message'] = "{} Successfully Logout".format(user_data.username)
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def city_data_view(request, page=1):
    try:
        city_data = alldata(City, page)
        if city_data[0] is not None:
            category_data_list = []
            for i in city_data[0]:
                j = model_to_dict(i)
                if i.state_id:
                    j['state_id'] = i.state_id.state_name
                else:
                    j['state_id'] = ''
                if i.city_image:
                    j['city_image'] = i.city_image.url
                else:
                    j['city_image'] = ''
                for k in j:
                    if j[k] is None:
                        j[k] = ''
                category_data_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all City data"
            return_json['count_result'] = 1
            return_json['data'] = category_data_list
        return JsonResponse(return_json, safe=False, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
@decorator_from_middleware(LoginWithOtpSendMiddleware)
def login_with_otp_send(request, form=None):
    try:
        if request.method == 'POST':
            mobile_or_email = form.cleaned_data.get('mobile_or_email')
            if Register.objects.filter(mobile=mobile_or_email, is_mobile=True):
                user_data = Register.objects.get(mobile=mobile_or_email, is_mobile=True)
                otp_response = token_sms(user_data.mobile)
                return JsonResponse(otp_response, safe=False, status=200)
            elif Register.objects.filter(email=mobile_or_email, is_email=True):
                user_data = Register.objects.get(email=mobile_or_email, is_email=True)
                otp = email_send_otp_generate(user_data)
                html_ = email_send_otp_html(otp)
                if isinstance(html_, dict):
                    return_json_ = html_
                else:
                    return_json_ = email_send(user_data, f'{otp} is Electrotrade Verification Code For Login', html_)
                return JsonResponse(return_json_, status=200, safe=False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
@decorator_from_middleware(LoginWithOtpVerifyMiddleware)
def login_with_otp_verify(request, form=None):
    if request.method == 'POST':
        mobile_or_email = form.cleaned_data.get('mobile_or_email')
        otp = form.cleaned_data.get('otp')
        is_otp_verify = False
        user_data = None
        if len(otp) == 4:
            if Register.objects.filter(mobile=mobile_or_email, is_mobile=True).exists():
                user_data = Register.objects.get(mobile=mobile_or_email, is_mobile=True)
                otp_response = verify(user_data.mobile, otp)
                if otp_response['valid'] and otp_response['message'] == "SMS request successfully verify":
                    is_otp_verify = True
            else:
                return_json['valid'] = False
                return_json['message'] = f"Login Account Not Valid"
                return_json['count_result'] = 1
                return_json['data'] = None
                return JsonResponse(return_json, status=200, safe=False)
        if len(otp) == 6:
            if Register.objects.filter(email=mobile_or_email, is_email=True, key=otp).exists():
                user_data = Register.objects.get(email=mobile_or_email, is_email=True, key=otp)
                user_data.key = None
                user_data.updated_at = datetime.now()
                user_data.save()
                is_otp_verify = True
            else:
                return_json['valid'] = False
                return_json['message'] = f"Login Account Not Valid"
                return_json['count_result'] = 1
                return_json['data'] = None
                return JsonResponse(return_json, status=200, safe=False)
        if is_otp_verify:
            try:
                if user_data is not None:

                    token = jwt.encode({
                        'account_id': user_data.account_id,
                        'username': user_data.username,
                        'token_created_at': str(datetime.now()),
                        'a': {2: True}},
                        token_key["token_key"],
                        algorithm='HS256'
                    )
                    user_data.token = token.decode()
                    user_data.last_login = datetime.now()
                    user_data.key = None
                    user_data.save()
                    users_data = UserInfo(user_data)
                    if UserCategory.objects.filter(user=user_data).exists():
                        category_data = UserCategory.objects.get(user=user_data)
                        users_data['Category'] = category_data.list_category
                    else:
                        users_data['Category'] = [""]
                    return_json['valid'] = True
                    return_json['message'] = "Successfully Login"
                    return_json['count_result'] = 1
                    return_json['data'] = users_data
                    return JsonResponse(return_json, safe=False, status=200)
                else:
                    return_json['valid'] = False
                    return_json['message'] = "Incorrect username and password"
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    return JsonResponse(return_json, status=200, safe=False)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
                return_json['valid'] = False
                return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
                return_json['count_result'] = 1
                return_json['data'] = None
                return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def verify_mobile_view(request):
    try:
        if request.method == 'POST':
            user_data = Register.objects.get(account_id=request.COOKIES['id'])
            otp = request.POST.get('otp')
            otp_response = verify(user_data.mobile, otp)
            if otp_response['valid'] and otp_response['message'] == "SMS request successfully verify":
                user_data.is_mobile = True
                user_data.updated_at = datetime.now()
                user_data.save()
                return_json['valid'] = True
                return_json['message'] = "Successfully User Mobile Verified"
                return_json['count_result'] = 1
                return_json['data'] = UserInfo(Register.objects.get(account_id=request.COOKIES['id']))
                otp_response = return_json
            return JsonResponse(otp_response, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def verify_email_otp_send_view(request):
    try:
        user_data = Register.objects.get(account_id=request.COOKIES['id'])
        otp = email_send_otp_generate(user_data)
        html_ = email_send_otp_html(otp)
        if isinstance(html_, dict):
            return_json_ = html_
        else:
            return_json_ = email_send(user_data, f'{otp} is Electrotrade Verification Code For Email Verification',
                                      html_)
        return JsonResponse(return_json_, status=200, safe=False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def verify_email_otp_verify_view(request):
    try:
        if request.method == 'POST':
            user_data = Register.objects.get(account_id=request.COOKIES['id'])
            otp = request.POST.get('otp')
            if user_data.key == otp:
                user_data.is_email = True
                user_data.key = None
                user_data.updated_at = datetime.now()
                user_data.save()
                return_json['valid'] = True
                return_json['message'] = "Successfully User Mobile Verified"
                return_json['count_result'] = 1
                return_json['data'] = UserInfo(Register.objects.get(account_id=request.COOKIES['id']))
            else:
                return_json['valid'] = False
                return_json['message'] = f"Failed to verify email"
                return_json['count_result'] = 0
                return_json['data'] = None
            return JsonResponse(return_json, status=200, safe=False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


