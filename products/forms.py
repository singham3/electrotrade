from django import forms
from .models import *
from electonicswebservice.admininfo import *
from django.forms import BaseModelForm, ModelForm
import sys
from django_mysql.forms import SimpleListField


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.title)


class BannerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.id)


class ProductSpecForm(ModelForm):
    product = ProductChoiceField(queryset=Products.objects.all(), required=True)
    title = forms.ChoiceField(choices=product_spec_choices, initial='Technical Specification', required=True)
    description = forms.CharField(widget=forms.Textarea(), required=True, initial={" ": " "})
    second_title = forms.ChoiceField(choices=product_spec_choices, initial='General Specification', required=False)
    second_description = forms.CharField(widget=forms.Textarea(), required=False, initial={" ": " "})
    third_title = forms.ChoiceField(choices=product_spec_choices, initial='Design Specification', required=False)
    third_description = forms.CharField(widget=forms.Textarea(), required=False, initial={" ": " "})

    class Meta:
        model = ProductSpec
        fields = ('product', 'title', 'description', 'second_title', 'second_description', 'third_title',
                  'third_description')

    def clean(self):
        try:
            cleaned_data = super(ProductSpecForm, self).clean()
            description = eval(cleaned_data.get("description"))
            if cleaned_data.get("second_description"):
                second_description = eval(cleaned_data.get("second_description"))
            if cleaned_data.get("third_description"):
                third_description = eval(cleaned_data.get("third_description"))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            raise forms.ValidationError(f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductsForm(ModelForm):
    image = forms.FileField(required=True)  # file filed
    image_slave_one = forms.ImageField(required=False)
    image_slave_two = forms.ImageField(required=False)
    image_slave_three = forms.ImageField(required=False)
    image_slave_four = forms.ImageField(required=False)
    gst_per = forms.FloatField(required=False)

    class Meta:
        model = Products
        fields = ('title', 'slug', 'model_number', 'serial_number', 'category', 'brand',
                  'description', 'actual_price', 'selling_price', 'image', 'image_slave_one', 'image_slave_two',
                  'image_slave_three', 'image_slave_four', 'gst_per', 'in_offer', 'minimum_qty', 'rewards',
                  'delivery_days', 'delivery_charges', 'is_trading', 'is_latest', 'status', 'timestamp')


class ProductReviewForm(ModelForm):
    title = forms.CharField(required=True)
    comment = forms.CharField(widget=forms.TextInput(), required=True)
    rating = forms.CharField(required=True)

    class Meta:
        model = ProductReview
        fields = ('title', 'comment', 'rating')

    def clean(self):
        cleaned_data = super(ProductReviewForm, self).clean()
        rating = cleaned_data.get("rating")
        if rating not in ['1', '2', '3', '4', '5']:
            raise forms.ValidationError("Rating must be valid value in 1-5")
        else:
            return cleaned_data


class OrderForm(ModelForm):
    total = forms.CharField(required=True)
    status = forms.CharField(required=True)
    product_id = forms.CharField(required=True)

    class Meta:
        model = AddCart
        fields = ('total', 'status', 'product_id')

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        try:
            total = int(cleaned_data.get("total"))
            product_id = cleaned_data.get("product_id")
            if not Products.objects.filter(id=product_id).exists():
                raise forms.ValidationError("Product Not Exist")
            minimum_qty = Products.objects.get(id=product_id).minimum_qty
            if total < minimum_qty:
                raise forms.ValidationError(f"Product quantity must be more then minimum limit {minimum_qty}")
            return cleaned_data

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            raise forms.ValidationError(f"{e}")


class ProductOrderForm(ModelForm):
    order_id = forms.CharField(required=True)
    reward = forms.BooleanField(required=True)
    payment_method = forms.CharField(required=True)

    class Meta:
        model = OrderProduct
        fields = ('order_id', 'reward', 'payment_method')

    def clean(self):
        cleaned_data = super(ProductOrderForm, self).clean()
        order_id = cleaned_data.get("order_id")
        if not AddCart.objects.filter(order=OrderId.objects.get(order_id=order_id)).exists():
            raise forms.ValidationError("Order Not Exists")
        else:
            return cleaned_data


class UserCategoryForm(ModelForm):
    category_list = SimpleListField(forms.IntegerField(), required=True)

    class Meta:
        model = UserCategory
        fields = ('category_list', )

    def clean(self):
        cleaned_data = super(UserCategoryForm, self).clean()
        category_list = cleaned_data.get("category_list")
        if category_list is None:
            return None
        for i in category_list:
            if not Category.objects.filter(id=i).exists():
                raise forms.ValidationError(f"Category id {i} Not Exists")
        return cleaned_data


class RemoveCartForm(ModelForm):
    order_id = forms.CharField(required=True)
    product_id = forms.CharField(required=True)

    class Meta:
        model = AddCart
        fields = ('order_id', 'product_id')

    def clean(self):
        cleaned_data = super(RemoveCartForm, self).clean()
        order_id = cleaned_data.get("order_id")
        product_id = cleaned_data.get("product_id")
        if not AddCart.objects.filter(order=OrderId.objects.get(order_id=order_id)).exists():
            raise forms.ValidationError("Order Not Exists")
        if not AddCart.objects.filter(product=product_id).exists():
            raise forms.ValidationError("Product Not Add in Cart")
        return cleaned_data


class BannerProductsForm(ModelForm):
    banner_id = BannerChoiceField(queryset=Banner.objects.all(), required=True)
    product = ProductChoiceField(queryset=Products.objects.all(), required=True)

    class Meta:
        model = BannerProducts
        fields = ('banner_id', 'product')
