from django import forms
from products.models import *
from electonicswebservice.admininfo import *
from django.forms import BaseModelForm, ModelForm
import sys
from django_mysql.forms import SimpleListField


class ProductOrderAddressForm(ModelForm):
    address_id = forms.CharField(required=False)
    city_name = forms.CharField(required=True)
    state_name = forms.CharField(required=True)
    pincode = forms.CharField(required=True)
    address = forms.CharField(required=True)
    mobile_no = forms.CharField(required=False)

    class Meta:
        model = OrderAddress
        fields = ('address_id', 'city_name', 'state_name', 'pincode', 'address', 'mobile_no')

    def clean(self):
        cleaned_data = super(ProductOrderAddressForm, self).clean()
        city = cleaned_data.get("city_name")
        state = cleaned_data.get("state_name")
        logger.info('address_id' in cleaned_data, str(type(cleaned_data)))
        if 'address_id' in cleaned_data and cleaned_data.get("address_id"):
            address_id = cleaned_data.get("address_id")
            if not OrderAddress.objects.filter(id=int(address_id)).exists():
                raise forms.ValidationError("Order Address Not Exists")
        if not City.objects.filter(city_name=city).exists():
            raise forms.ValidationError("City Not Exists")
        if not State.objects.filter(state_name=state).exists():
            raise forms.ValidationError("State Not Exists")
        return cleaned_data


class ProductOrderSelectAddressForm(ModelForm):
    address_id = forms.CharField(required=True)

    class Meta:
        model = OrderAddress
        fields = ('address_id', )

    def clean(self):
        cleaned_data = super(ProductOrderSelectAddressForm, self).clean()
        address_id = int(cleaned_data.get("address_id"))
        if not OrderAddress.objects.filter(id=address_id).exists():
            raise forms.ValidationError("Order Address Not Exists")
        return cleaned_data
