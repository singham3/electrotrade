from django.contrib import admin
from .models import *
from electonicswebservice.admininfo import *
from .forms import *
# Register your models here.


class OTPHistoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class BannerAdminView(admin.ModelAdmin):
    def image(self, obj):
        return obj.image.url
    list_display = ('id', 'image', 'url', 'date_from', 'date_to', 'status', 'created_at')


class BannerProductsAdminView(admin.ModelAdmin):
    def banner(self, obj):
        return obj.banner_id.id

    def product_title(self, obj):
        return obj.product.title
    list_display = ('id', 'banner', 'product_title', 'created_at')
    form = BannerProductsForm


class CategoryAdminView(admin.ModelAdmin):
    def image(self, obj):
        return obj.image.url

    list_display = ('id', 'title', 'image', 'created_at')
    
    
class BrandAdminView(admin.ModelAdmin):
    def logo(self, obj):
        return obj.logo.url

    list_display = ('id', 'name', 'logo', 'created_at')


class ServiceEngineerAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ServiceEnquiryAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ServiceReviewAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ServiceRewardAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    
    
class ProductsAdminView(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'brand', 'selling_price', 'image',
                    'image_slave_one', 'image_slave_two', 'image_slave_three', 'image_slave_four', 'status',
                    'created_at')
    form = ProductsForm


class ProductReviewAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductSpecAdminView(admin.ModelAdmin):
    def product_detail(self, obj):
        if obj.product is not None:
            return obj.product.title

    def product_id(self, obj):
        if obj.product is not None:
            return obj.product.id
    list_display = ('id', 'title', 'second_title', 'third_title', 'product_id', 'product_detail', 'created_at')
    form = ProductSpecForm


class AddCartAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class OrderProductAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class OrderAddressAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductRewardAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class RewardRedeemAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductsPaymentMethodAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductPaymentsAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductIGSTAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class UserCategoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


admin.site.register(OTPHistory, OTPHistoryAdminView)
admin.site.register(Banner, BannerAdminView)
admin.site.register(Category, CategoryAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(ServiceEngineer, ServiceEngineerAdminView)
admin.site.register(ServiceEnquiry, ServiceEnquiryAdminView)
admin.site.register(ServiceReview, ServiceReviewAdminView)
admin.site.register(ServiceReward, ServiceRewardAdminView)
admin.site.register(Products, ProductsAdminView)
admin.site.register(ProductReview, ProductReviewAdminView)
admin.site.register(ProductSpec, ProductSpecAdminView)
admin.site.register(AddCart, AddCartAdminView)
admin.site.register(OrderProduct, OrderProductAdminView)
admin.site.register(OrderAddress, OrderAddressAdminView)
admin.site.register(ProductReward, ProductRewardAdminView)
admin.site.register(RewardRedeem, RewardRedeemAdminView)
admin.site.register(BannerProducts, BannerProductsAdminView)
admin.site.register(ProductsPaymentMethod, ProductsPaymentMethodAdminView)
admin.site.register(ProductPayments, ProductPaymentsAdminView)
admin.site.register(ProductIGST, ProductIGSTAdminView)
admin.site.register(UserCategory, UserCategoryAdminView)

