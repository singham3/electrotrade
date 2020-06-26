from django.db import models
from datetime import datetime
from tinymce.models import HTMLField
from registration.models import *
from django_mysql.models import ListCharField


banner_section_choices = [('1', '1'), ('2', '2'), ('3', '3')]
replacement_duration_choices = [('1 Month', 1), ('2 Months', 2), ('3 Months', 3), ('4 Months', 4),
                                ('5 Months', 5), ('6 Months', 6), ('7 Months', 7), ('8 Months', 8),
                                ('9 Months', 9), ('10 Months', 10), ('11 Months', 11), ('12 Months', 12),
                                ('2 Years', 24), ('3 Years', 36)]
product_spec_choices = [('Technical Specification', 'Technical Specification'),
                        ('General Specification', 'General Specification'),
                        ('Design Specification', 'Design Specification')]

delivery_status_choices = [('Your Order Has Placed', 'Your Order Has Placed'),
                           ('Order Shipped', 'Order Shipped'),
                           ('Out for delivery', 'Out for delivery'),
                           ('Delivered', 'Delivered')]

payment_status_choices = [('Unpaid', 'Unpaid'), ('Paid', 'Paid')]


class Banner(models.Model):
    image = models.ImageField(upload_to='products/banner/')
    url = models.URLField(null=True, blank=True)
    validation = models.DateTimeField(default=datetime.now)
    banner_section = models.CharField(max_length=250, choices=banner_section_choices, null=True, blank=True)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "banners"


class Category(models.Model):
    title = models.CharField(max_length=200, default=None)
    slug = models.SlugField(max_length=40, unique=False)
    image = models.ImageField(upload_to='products/category/')
    timestamp = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"


class UserCategory(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    list_category = ListCharField(base_field=models.CharField(max_length=10), size=6, max_length=(6 * 11))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Brand(models.Model):
    name = models.CharField(max_length=200, default=None)
    logo = models.ImageField(upload_to='products/brand/')
    is_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "brands"


# Service models start
class ServiceEngineer(models.Model):
    name = models.CharField(max_length=200, default=None)
    mobile = models.IntegerField(default=None)
    specialist = models.CharField(max_length=200, default=None)
    address = models.CharField(max_length=200, default=None)
    govt_id = models.CharField(max_length=200, default=None)
    charges = models.FloatField(default=None)
    commission = models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ServiceEngineers"


class ServiceEnquiry(models.Model):
    service_eng = models.ForeignKey(ServiceEngineer, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=200, default=None)
    contact_num = models.IntegerField(default=None)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    pincode = models.IntegerField(default=None)
    address = models.TextField(max_length=550, default=None)
    product = models.TextField(max_length=550, default=None)
    rp_before = models.FileField(upload_to='products/serviceEnquiry/', blank=False)
    rp_after = models.FileField(upload_to='products/serviceEnquiry/', blank=False)
    status = models.CharField(max_length=200, default=None)
    sec_acceptance = models.CharField(max_length=200, default="NO")
    timestamp = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ServiceEnquiries"


class ServiceReview(models.Model):
    service_enq = models.ForeignKey(ServiceEnquiry, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100, default=None)
    rating = models.FloatField(default=None)
    slug = models.CharField(max_length=200, default=None)
    comment = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ServiceReviews"


class ServiceReward(models.Model):
    service = models.ForeignKey(ServiceEnquiry, on_delete=models.PROTECT, null=True)
    reward_point = models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ServiceRewards"


class Products(models.Model):
    title = models.CharField(max_length=255, default="products", null=False, blank=False)
    model_number = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=40, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True)
    description = HTMLField()
    actual_price = models.FloatField(null=True, default=None)
    selling_price = models.FloatField(null=True, default=None)
    image = models.FileField(upload_to='products/', blank=True)  # file filed
    image_slave_one = models.ImageField(upload_to='products/', blank=True)
    image_slave_two = models.ImageField(upload_to='products/', blank=True)
    image_slave_three = models.ImageField(upload_to='products/', blank=True)
    image_slave_four = models.ImageField(upload_to='products/', blank=True)
    gst_per = models.FloatField(default=None, null=True, blank=True)
    in_offer = models.CharField(max_length=200, null=True, blank=True)
    minimum_qty = models.IntegerField(default=0)
    rewards = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    delivery_days = models.IntegerField(default=5)
    delivery_charges = models.FloatField(default=0.0)
    buy_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=datetime.now)
    is_replacement = models.BooleanField(default=False)
    replacement_duration = models.IntegerField(default=0, choices=replacement_duration_choices)
    is_trading = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "products"

    def get_products(self):
        return "\n".join([c.categories for c in self.category.all()])


class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    comment = models.TextField(null=True, default=None)
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ProductReviews"


class ProductSpec(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=200, choices=product_spec_choices, default=None)
    description = models.TextField(max_length=20000, default=None)
    second_title = models.CharField(max_length=200, choices=product_spec_choices, default=None)
    second_description = models.TextField(max_length=20000, default=None)
    third_title = models.CharField(max_length=200, choices=product_spec_choices, default=None)
    third_description = models.TextField(max_length=20000, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ProductSpecs"


class OrderId(models.Model):
    order_id = models.IntegerField(default=randint(10**(8-1), (10**8)-1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductIGST(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, unique=True)
    igst_value = models.FloatField(default=None)
    igst_per = models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


# master  user order table
class AddCart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    gst_value = models.FloatField(default=None)
    total = models.FloatField(default=None)
    per_product_price = models.FloatField(default=None)
    total_after_tax = models.FloatField(default=None)
    delivery_charges = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=200, default=None)
    order = models.ForeignKey(OrderId, on_delete=models.PROTECT, null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Orders"


class OrderAddress(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True)
    pincode = models.IntegerField(default=None, null=True, blank=True)
    address = models.TextField(max_length=550, default=None, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    is_profile = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "OrderAddress"


class OrderProduct(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(OrderId, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    price = models.FloatField(default=None)
    quantity = models.IntegerField(default=None)
    gst_per = models.FloatField(default=None)
    total_after_tax = models.FloatField(default=None)
    delivery_days = models.IntegerField(default=5)
    delivery_date_time = models.DateTimeField(null=True, blank=True)
    delivery_charges = models.FloatField(null=True, blank=True)
    delivery_status = models.CharField(max_length=200, default="Your Order Has Placed")
    delivery_address = models.ForeignKey(OrderAddress, on_delete=models.PROTECT, null=True)
    is_replacement = models.BooleanField(default=False)
    replacement_from = models.DateTimeField(null=True, blank=True)
    replacement_to = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    order_cancel_date_time = models.DateTimeField(null=True, blank=True)
    cancellation_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "OrderProducts"


class ProductReward(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    reward_point = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ProductRewards"


class RewardRedeem(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    points = models.FloatField(default=0.0)
    order = models.ForeignKey(OrderId, on_delete=models.PROTECT, null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "RewardRedeems"


class BannerProducts(models.Model):
    banner_id = models.ForeignKey(Banner, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductFilter(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    filter_title = models.CharField(max_length=250)
    filter_value = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ProductFilter"


class ProductsPaymentMethod(models.Model):
    method = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductPayments(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT)
    order = models.ForeignKey(OrderId, on_delete=models.PROTECT)
    total_after_tax = models.FloatField(default=0.0)
    reward = models.ForeignKey(ProductReward, on_delete=models.PROTECT, null=True, blank=True)
    total_products_price = models.FloatField(default=0.0)
    payment_method = models.ForeignKey(ProductsPaymentMethod, on_delete=models.PROTECT)
    payment_status = models.CharField(max_length=250)
    is_cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class OrderProductDeliver(models.Model):
    user = models.ForeignKey(Register, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(OrderId, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True)
    order_product = models.ForeignKey(OrderProduct, on_delete=models.PROTECT, null=True)
    product_price = models.FloatField(default=0.0, null=True, blank=True)
    payment_status = models.CharField(max_length=250, null=True, blank=True)
    payment_method = models.ForeignKey(ProductsPaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    delivery_amount = models.FloatField(default=0.0)
    delivery_date_time = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=200, choices=delivery_status_choices, default="Your Order Has Placed")
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
