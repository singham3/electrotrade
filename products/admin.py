from django.contrib import admin
from .models import *
from electonicswebservice.admininfo import *
from .forms import *
from django.contrib import messages


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

    list_display = ('id', 'title', 'category', 'brand', 'selling_price',  'status', 'rewards', 'minimum_qty', 'created_at')
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


class OrderProductAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class OrderProductDeliverAdminView(admin.ModelAdmin):
    def product_detail(self, obj):
        if obj.product is not None:
            return obj.product.title

    def order_detail(self, obj):
        if obj.order is not None:
            return obj.order.order_id

    def order_product_detail(self, obj):
        if obj.order_product is not None:
            return obj.order_product.id
    list_display = ('id', 'order_detail', 'product_detail', 'order_product_detail', 'is_delivered',
                    'delivery_date_time', 'delivery_status')
    form = OrderProductDeliverform

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            try:
                if form.is_valid():
                    user = form.cleaned_data["user"]
                    order = form.cleaned_data['order']
                    product = form.cleaned_data['product']
                    order_product = form.cleaned_data['order_product']
                    payment_status = form.cleaned_data['payment_status']
                    delivery_amount = form.cleaned_data.get('delivery_amount')
                    delivery_date_time = form.cleaned_data.get('delivery_date_time')
                    delivery_status = form.cleaned_data.get('delivery_status')
                    is_delivered = form.cleaned_data.get('is_delivered')
                    
                    order_product_obj = OrderProduct.objects.get(id=order_product.id, user=user, product=product,
                                                                 order=order, is_cancel=False)
                    order_product_deliver = OrderProductDeliver.objects.get(user=user, product=product, order=order,
                                                                            order_product=order_product)
                    if order_product_deliver.payment_status == 'Paid' and order_product_deliver.delivery_amount > 0.0 and order_product_deliver.delivery_status == 'Delivered' and order_product_deliver.is_delivered == True:
                        messages.info(request, f'Order {order.order_id} Already delivered !!!!!')
                    else:
                        if delivery_amount and delivery_status == 'Delivered' and order_product_obj.total_after_tax == delivery_amount and payment_status == 'Paid':
                            order_product_deliver.payment_status = payment_status
                            order_product_deliver.delivery_amount = delivery_amount
                            order_product_deliver.delivery_status = delivery_status
                            order_product_deliver.is_delivered = is_delivered
                            product_reward = ProductReward.objects.get(user=user)
                            product_reward.reward_point += order_product_obj.product.rewards
                            product_reward.updated_at = datetime.now()
                            product_reward.save()
                            product_payment = ProductPayments.objects.get(order=order,
                                                                          is_cancel=False)
                            product_payment.payment_status = payment_status
                            product_payment.updated_at = datetime.now()
                            product_payment.save()
                        else:
                            order_product_deliver.delivery_status = delivery_status
                    order_product_deliver.delivery_date_time = delivery_date_time
                    order_product_deliver.updated_at = datetime.now()
                    order_product_deliver.save()
                    order_product_obj.delivery_date_time = delivery_date_time
                    order_product_obj.delivery_status = delivery_status
                    order_product_obj.is_delivered = is_delivered
                    order_product_obj.updated_at = datetime.now()
                    order_product_obj.save()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
                messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class ProductsPaymentMethodAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class ProductIGSTAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class UserCategoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')


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
admin.site.register(OrderProduct, OrderProductAdminView)
admin.site.register(OrderProductDeliver, OrderProductDeliverAdminView)
admin.site.register(BannerProducts, BannerProductsAdminView)
admin.site.register(ProductsPaymentMethod, ProductsPaymentMethodAdminView)
admin.site.register(ProductIGST, ProductIGSTAdminView)
admin.site.register(UserCategory, UserCategoryAdminView)

