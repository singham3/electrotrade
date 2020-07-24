from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from random import randint
import hashlib
from django.forms.models import model_to_dict
from authy.api import AuthyApiClient
from django.conf import settings
from electonicswebservice.otpsend import *
from products.models import *
import os, sys


class CreateUserService(Service):
    password = forms.CharField(required=False)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(required=True)
    gender = forms.CharField(required=False)
    role = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    user_profile_img = forms.ImageField(required=False)
    account_id = forms.CharField(required=False)
    is_active = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    pincode = forms.CharField(required=False)
    gst_number = forms.CharField(required=False)
    document_type = forms.CharField(required=False)
    varification_document_front = forms.FileField(required=False)
    varification_document_back = forms.FileField(required=False)
    business_type = forms.CharField(required=False)
    business_name = forms.CharField(required=False)
    business_description = forms.CharField(required=False)
    alternate_mobile = forms.CharField(required=False)
    status = forms.CharField(required=False)

    def process(self):
        try:
            _date_of_birth = datetime.strptime(str(self.cleaned_data["date_of_birth"]), '%Y-%m-%d') if self.cleaned_data["date_of_birth"] else None
            _user_profile_img = self.cleaned_data["user_profile_img"] if self.cleaned_data["user_profile_img"] else None
            _account_id = self.cleaned_data["account_id"] if self.cleaned_data["account_id"] else randint(10**(8-1), (10**8)-1)
            _city = City.objects.get(id=self.cleaned_data["city"]) if self.cleaned_data["city"] else None
            _state = State.objects.get(id=self.cleaned_data["state"]) if self.cleaned_data["state"] else None
            _address = self.cleaned_data["address"] if self.cleaned_data["address"] else None
            _pincode = self.cleaned_data["pincode"] if self.cleaned_data["pincode"] else None
            _document_type = DocumentType.objects.get(id=self.cleaned_data["document_type"]) if self.cleaned_data["document_type"] else None
            _varification_document_front = self.cleaned_data["varification_document_front"] if self.cleaned_data["varification_document_front"] else None
            _varification_document_back = self.cleaned_data["varification_document_back"] if self.cleaned_data["varification_document_back"] else None
            _status = True if self.cleaned_data["status"] else True
            _gst_number = self.cleaned_data["gst_number"] if self.cleaned_data["gst_number"] else None
            _gender = Gender.objects.get(id=self.cleaned_data["gender"]) if self.cleaned_data["gender"] else None
            _role = Role.objects.get(id=self.cleaned_data["role"]) if self.cleaned_data["role"] else Role.objects.get(role_name='User')
            _is_active = True if self.cleaned_data["is_active"] else False
            business_type = BusinessType.objects.get(id=self.cleaned_data["business_type"]) if self.cleaned_data["business_type"] else None
            business_name = self.cleaned_data["business_name"]
            business_description = self.cleaned_data["business_description"]
            alternate_mobile = self.cleaned_data["alternate_mobile"]
            if Register.objects.filter(username=self.cleaned_data["username"], account_id=_account_id).exists():
                user_data = Register.objects.get(username=self.cleaned_data["username"])
                if self.cleaned_data["password"]:
                    user_data.password = hashlib.sha256(self.cleaned_data["password"].encode()).hexdigest()
                user_data.is_active = _is_active
                user_data.gender = _gender
                user_data.role = _role
                user_data.date_of_birth = _date_of_birth
                user_data.user_profile_img = _user_profile_img
                user_data.city = _city
                user_data.state = _state
                user_data.address = _address
                user_data.pincode = _pincode
                user_data.gst_number = _gst_number
                user_data.document_type = _document_type
                if self.cleaned_data["mobile"]:
                    user_data.mobile = self.cleaned_data["mobile"]
                    user_data.is_mobile = False
                if self.cleaned_data["email"]:
                    user_data.email = self.cleaned_data["email"]
                    user_data.is_email = False
                user_data.varification_document_front = _varification_document_front
                user_data.varification_document_back = _varification_document_back
                user_data.status = bool(_status)
                user_data.updated_at = datetime.now()
                user_data.business_type = business_type
                user_data.business_name = business_name
                user_data.business_description = business_description
                user_data.alternate_mobile = alternate_mobile
                user_data.save()
                if OrderAddress.objects.filter(user=Register.objects.get(username=self.cleaned_data["username"]), is_profile=True).exists():
                    order_address = OrderAddress.objects.get(user=Register.objects.get(username=self.cleaned_data["username"]),
                                                             is_profile=True)
                    order_address.city = _city
                    order_address.state = _state
                    order_address.address = _address
                    order_address.pincode = _pincode
                    order_address.save()
                return Register.objects.get(username=self.cleaned_data["username"])
            else:
                Register(password=hashlib.sha256(self.cleaned_data["password"].encode()).hexdigest(),
                         username=self.cleaned_data["username"],
                         first_name=self.cleaned_data["first_name"],
                         last_name=self.cleaned_data["last_name"],
                         email=self.cleaned_data["email"],
                         is_active=_is_active,
                         gender=_gender,
                         role=_role,
                         mobile=self.cleaned_data["mobile"],
                         date_of_birth=_date_of_birth,
                         user_profile_img=_user_profile_img,
                         account_id=_account_id,
                         city=_city,
                         state=_state,
                         address=_address,
                         pincode=_pincode,
                         gst_number=_gst_number,
                         document_type=_document_type,
                         varification_document_front=_varification_document_front,
                         varification_document_back=_varification_document_back,
                         status=bool(_status),
                         business_type=business_type,
                         business_name=business_name,
                         business_description=business_description,
                         alternate_mobile=alternate_mobile,
                         ).save()
                user = Register.objects.last()
                if _city and _state and _address and _pincode:
                    OrderAddress(user=user, city=_city, state=_state, address=_address, pincode=_pincode,
                                 is_profile=True).save()
                return Register.objects.last()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return f"{e}, {f_name}, {exc_tb.tb_lineno}"
