from django import forms
from .models import *
from electonicswebservice.admininfo import *
from django.forms import BaseModelForm, ModelForm
import sys


class SearchForm(ModelForm):
    search = forms.CharField(required=True)

    class Meta:
        model = Search
        fields = ('search', )

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        return cleaned_data


class EnquiryFormForm(ModelForm):
    product_name = forms.CharField(required=True)
    product_company = forms.CharField(required=False)
    product_series_num = forms.CharField(required=False)
    prod_description = forms.CharField(required=True, widget=forms.TextInput)

    class Meta:
        model = EnquiryForm
        fields = ('product_name', 'product_company', 'product_series_num', 'prod_description')

    def clean(self):
        cleaned_data = super(EnquiryFormForm, self).clean()
        return cleaned_data
