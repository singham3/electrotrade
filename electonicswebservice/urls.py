"""electonicswebservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from registration.views import *
from products.views import *
from products.place_order.views import *
from search.views import *
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/user/login/', user_login),
    path('api/v1/user/logout/', user_logout_view),
    path('api/v1/user/forgot-password/', forget_password),
    path('api/v1/user/forgot-password/referral/', verify_forget_password),
    path('api/v1/user/profile/', user_profile),
    path('api/v1/user/city/', city_data_view),
    path('api/v1/products/category/', category_data_view),
    path('api/v1/products/category/<int:page>/', category_data_view),
    path('api/v1/products/brands/', brand_data_view),
    path('api/v1/products/brands/<int:page>/', brand_data_view),
    path('api/v1/products/', products_data_view),
    path('api/v1/latest-products/', latest_product_data_view),
    path('api/v1/products/<int:page>/', products_data_view),
    path('api/v1/products/banner/', banner_data_view),
    path('api/v1/products/banner/<int:page>/', banner_data_view),
    path('api/v1/products/banner/details/', banner_response_data_view),
    path('api/v1/products/product-review/', product_review_view),
    path('api/v1/products/product-review/<int:id>/', product_review_view),
    path('api/v1/products/add-cart/', add_cart_view),
    path('api/v1/products/add-cart/remove-card/', remove_cart_view),
    path('api/v1/products/order/order-product/', order_product_view),
    path('api/v1/products/order/order-address/', product_order_address_view),
    path('api/v1/products/order/order-address/select/', product_order_select_address_view),
    path('api/v1/products/order/order-address/remove/', product_order_remove_address_view),
    path('api/v1/products/order/order-address/edit/', product_order_edit_address_view),
    path('api/v1/products/category-list/', user_category_list_view),
    path('api/v1/latest-products/', latest_product_data_view),
    path('api/v1/products/search/', search_view),
    path('api/v1/user/sms/otp/send/', sms_otp_send_view),
    path('api/v1/user/sms/otp/verify/', sms_otp_verify_view)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Electrotrade Administration"
admin.site.site_title = 'Electrotrade Administration'

