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
        mobile_no = cleaned_data.get("mobile_no")
        if len(mobile_no) < 10 or len(mobile_no) > 13:
            raise forms.ValidationError("Mobile No. not Correct!")
        else:
            if len(mobile_no) > 10 and '+91' not in mobile_no:
                raise forms.ValidationError("Mobile No. not Correct!")
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


class OrderProductCancelForm(ModelForm):
    order_id = forms.CharField(required=True)
    product_id = forms.CharField(required=True)
    cancellation_description = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = OrderAddress
        fields = ('order_id', 'product_id', 'cancellation_description')

    def clean(self):
        cleaned_data = super(OrderProductCancelForm, self).clean()
        order = OrderId.objects.get(order_id=cleaned_data.get("order_id"))
        product_id = Products.objects.get(id=cleaned_data.get("product_id"))
        if not OrderProduct.objects.filter(order=order, product_id=product_id, is_cancel=False).exists():
            raise forms.ValidationError("Order Not Exists")

        return cleaned_data
