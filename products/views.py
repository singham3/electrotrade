from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from electonicswebservice.admininfo import *
from .models import *
import sys
from .middleware import *
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .json_products import *


@api_view(['GET', 'POST'])
def user_delete(request, id=None):
    if Register.objects.filter(id=id).exists():
        user = Register.objects.get(id=id)

        if UserCategory.objects.filter(user=user).exists():
            for i in UserCategory.objects.filter(user=user):
                i.delete()
        if ServiceEnquiry.objects.filter(user=user).exists():
            for i in ServiceEnquiry.objects.filter(user=user):
                i.delete()
        if ProductReview.objects.filter(user=user).exists():
            for i in ProductReview.objects.filter(user=user):
                i.delete()
        if AddCart.objects.filter(user=user).exists():
            for i in AddCart.objects.filter(user=user):
                i.delete()
        if ProductReward.objects.filter(user=user).exists():
            for i in ProductReward.objects.filter(user=user):
                i.delete()
        if RewardRedeem.objects.filter(user=user).exists():
            for i in RewardRedeem.objects.filter(user=user):
                i.delete()
        if ProductPayments.objects.filter(user=user).exists():
            for i in ProductPayments.objects.filter(user=user):
                i.delete()
        if OrderProductDeliver.objects.filter(user=user).exists():
            for i in OrderProductDeliver.objects.filter(user=user):
                i.delete()
        if OrderProduct.objects.filter(user=user).exists():
            for i in OrderProduct.objects.filter(user=user):
                i.delete()
        if OrderAddress.objects.filter(user=user).exists():
            for i in OrderAddress.objects.filter(user=user):
                i.delete()
        user.delete()
        return_json['valid'] = True
        return_json['message'] = "User Successfully Delete"
        return_json['count_result'] = 1
        return_json['data'] = 'Done'
    else:
        return_json['valid'] = False
        return_json['message'] = "User not exists"
        return_json['count_result'] = 0
        return_json['data'] = 'User not exists'
    return JsonResponse(return_json, status=200)



@api_view(['GET', 'POST'])
def category_data_view(request, page=1):
    try:
        category_data = alldata(Category, page)
        if category_data[0] is not None:
            category_data_list = []
            for i in category_data[0]:
                j = model_to_dict(i)
                if i.image:
                    j['image'] = i.image.url
                else:
                    j['image'] = ''
                for k in j:
                    if j[k] is None:
                        j[k] = ''
                category_data_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all category data"
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
def brand_data_view(request, page=1):
    try:
        brand_data = Brand.objects.filter(is_show=True)
        paginator = Paginator(brand_data, 6)
        contacts = paginator.get_page(page)
        if contacts is not None:
            category_data_list = []
            for i in contacts:
                j = model_to_dict(i)
                if i.logo:
                    j['logo'] = i.logo.url
                else:
                    j['logo'] = ''
                for k in j:
                    if j[k] is None:
                        j[k] = ''
                category_data_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all brand data"
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
def products_data_view(request, page=1):
    try:
        if 'category' in request.GET:
            category = Category.objects.get(id=request.GET['category'])
        else:
            category = None
        if 'brand' in request.GET:
            brand = Brand.objects.get(id=request.GET['brand'])
        else:
            brand = None
        if 'id' in request.GET:
            product_id = int(request.GET['id'])
        else:
            product_id = None
        if category is not None and brand is not None:
            if product_id:
                product_data = Products.objects.filter(id=product_id, category=category, brand=brand)
            else:
                product_data = Products.objects.filter(category=category, brand=brand)
        elif category and brand is None:
            if product_id:
                product_data = Products.objects.filter(id=product_id, category=category)
            else:
                product_data = Products.objects.filter(category=category)
        elif brand and category is None:
            if product_id:
                product_data = Products.objects.filter(id=product_id, brand=brand)
            else:
                product_data = Products.objects.filter(brand=brand)
        else:
            if product_id:
                product_data = Products.objects.filter(id=product_id)
            else:
                product_data = Products.objects.filter()
        paginator = Paginator(product_data, 10)
        contacts = paginator.get_page(page)
        if contacts is not None:
            product_data_list = []
            for i in contacts:
                j = product_data_json(i)
                product_review_list = []
                if ProductReview.objects.filter(product=i.id).exists():
                    product_review = ProductReview.objects.filter(product=i.id)

                    for review in product_review:
                        review = model_to_dict(review)
                        for l in review:
                            if review[l] is None:
                                review[l] = ''
                        product_review_list.append(review)
                j['ProductReview'] = product_review_list
                if ProductSpec.objects.filter(product=i).exists():
                    j['ProductSpecification'] = product_spec_json(ProductSpec.objects.filter(product=i))
                else:
                    j['ProductSpecification'] = []

                for k in j:
                    if j[k] is None:
                        j[k] = ''
                product_data_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all brand data"
            return_json['count_result'] = 1
            return_json['data'] = product_data_list
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
def latest_product_data_view(request, page=1):
    category_data = UserCategory.objects.get(user=Register.objects.get(account_id=request.COOKIES['id']))
    latest_product_data = Products.objects.filter(category__in=category_data.list_category).order_by("-created_at")
    paginator = Paginator(latest_product_data, 4)
    contacts = paginator.get_page(page)
    products_dict = {}
    if contacts is not None:
        latest_product_data_list = []
        for i in contacts:
            j = product_data_json(i)
            if ProductSpec.objects.filter(product=i).exists():
                j['ProductSpecification'] = product_spec_json(ProductSpec.objects.filter(product=i))
            else:
                j['ProductSpecification'] = []
            latest_product_data_list.append(j)
        products_dict['Latest Product'] = latest_product_data_list
    trending_product_data = Products.objects.filter(category__in=category_data.list_category).order_by("-buy_count")
    trending_paginator = Paginator(latest_product_data, 3)
    trending_contacts = trending_paginator.get_page(page)
    trending_product_paginator = Paginator(trending_product_data, 3)
    trending_product_contacts = trending_product_paginator.get_page(page)
    if trending_contacts is not None and trending_product_contacts is not None:
        trending_product_data_list = []
        for i in trending_contacts:
            j = product_data_json(i)
            if ProductSpec.objects.filter(product=i).exists():
                j['ProductSpecification'] = product_spec_json(ProductSpec.objects.filter(product=i))
            else:
                j['ProductSpecification'] = []
            trending_product_data_list.append(j)
        for k in trending_product_contacts:
            if k in trending_contacts:
                continue
            m = product_data_json(k)
            if ProductSpec.objects.filter(product=k).exists():
                m['ProductSpecification'] = product_spec_json(ProductSpec.objects.filter(product=k))
            else:
                m['ProductSpecification'] = []
            trending_product_data_list.append(m)
        products_dict['Trading Product'] = trending_product_data_list
    return_json['valid'] = True
    return_json['message'] = "Successfully get all brand data"
    return_json['count_result'] = 1
    return_json['data'] = products_dict
    return JsonResponse(return_json, safe=False, status=200)


@api_view(['GET', 'POST'])
def banner_data_view(request, page=1):
    try:
        all_model_data = Banner.objects.filter(status=True)
        paginator = Paginator(all_model_data, 10)
        contacts = paginator.get_page(page)
        if contacts is not None:
            banner_data_list = []
            for i in contacts:
                j = model_to_dict(i)
                if i.image:
                    j['image'] = i.image.url
                else:
                    j['image'] = ''
                for k in j:
                    if j[k] is None:
                        j[k] = ''
                banner_data_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all Banner data"
            return_json['count_result'] = 1
            return_json['data'] = banner_data_list
        return JsonResponse(return_json, safe=False, status=200)
    except Exception as e:
        return_json['valid'] = False
        return_json['message'] = f"{e}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)


@api_view(['GET', 'POST'])
def banner_response_data_view(request):
    try:
        if 'id' in request.GET and request.GET['id'] is not None:
            id = request.GET['id']
            if BannerProducts.objects.filter(banner_id=Banner.objects.get(id=id)).exists():
                model_data_list = []
                model_data = BannerProducts.objects.filter(banner_id=Banner.objects.get(id=id))
                for i in model_data:
                    j = model_to_dict(i)
                    if i.banner_id:
                        j['banner_id'] = str(i.banner_id.id)
                    else:
                        j['banner_id'] = ""
                    if i.product:
                        j['product'] = product_data_json(i.product)
                    else:
                        j['product'] = []
                    for k in j:
                        if j[k] is None:
                            j[k] = ''
                    model_data_list.append(j)
                return_json['valid'] = True
                return_json['message'] = "Successfully get all Banner data"
                return_json['count_result'] = 1
                return_json['data'] = model_data_list
            else:
                return_json['valid'] = False
                return_json['message'] = "Banner Products not exists"
                return_json['count_result'] = 0
                return_json['data'] = "Banner Products not exists"
        else:
            return_json['valid'] = False
            return_json['message'] = "Banner id can not be None"
            return_json['count_result'] = 0
            return_json['data'] = "Banner id can not be None"
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
@decorator_from_middleware(ProductReviewMiddleware)
def product_review_view(request, id=None, form=None):
    try:
        if request.method == 'POST':
            user = Register.objects.get(account_id=request.COOKIES['id'])
            product = Products.objects.get(title=form.cleaned_data['title'])
            if ProductReview.objects.filter(product=product, user=user).exists():
                product_review = ProductReview.objects.get(product=product, user=user)
                product_review.comment = form.cleaned_data['comment']
                product_review.rating = int(form.cleaned_data['rating'])
                product_review.save()
                product_review = ProductReview.objects.get(product=product, user=user)
            else:
                product_review = ProductReview(product=product, user=user, comment=form.cleaned_data['comment'],
                                               rating=int(form.cleaned_data['rating']))
                product_review.save()
                product_review = ProductReview.objects.last()
            j = model_to_dict(product_review)
            for k in j:
                if j[k] is None:
                    j[k] = ''
            return_json['valid'] = True
            return_json['message'] = "Successfully get all product review data"
            return_json['count_result'] = 1
            return_json['data'] = j
            return JsonResponse(return_json, safe=False, status=200)
        else:
            if id is not None and id != '0' and id != '' and id != 0:
                try:
                    all_product_review = ProductReview.objects.filter(product=Products.objects.get(id=id))
                    all_product_review_list = []
                    for i in all_product_review:
                        j = model_to_dict(i)
                        for k in j:
                            if j[k] is None:
                                j[k] = ''
                        all_product_review_list.append(j)
                    return_json['valid'] = True
                    return_json['message'] = "Successfully get all product review data"
                    return_json['count_result'] = 1
                    return_json['data'] = all_product_review_list
                    return JsonResponse(return_json, safe=False, status=200)
                except ProductReview.DoesNotExist:
                    return_json['valid'] = False
                    return_json['message'] = 'Product Id Does not Exist !!!!'
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    return JsonResponse(return_json, status=200, safe=False)
            else:
                return_json['valid'] = False
                return_json['message'] = 'Please Provide Product Id'
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
@decorator_from_middleware(OrderMiddleware)
def add_cart_view(request, form=None):
    try:
        user = Register.objects.get(account_id=request.COOKIES['id'])
        if request.method == 'POST':
            product = Products.objects.get(id=form.cleaned_data['product_id'])
            total = int(form.cleaned_data['total'])
            status = form.cleaned_data['status']
            gst_value = product.gst_per if product.gst_per else 0
            if product.delivery_charges:
                total_after_tax = (product.selling_price*total) + product.delivery_charges
            else:
                total_after_tax = product.selling_price * total
            if AddCart.objects.filter(user=user, product=product).exists():
                product_order = AddCart.objects.get(user=user, product=product)
                product_order.gst_value = gst_value
                product_order.total = total
                product_order.total_after_tax = total_after_tax
                product_order.status = status
                product_order.per_product_price = product.selling_price
                product_order.delivery_charges = product.delivery_charges
                product_order.save()
            else:
                if AddCart.objects.filter(user=user).exists():
                    order_id = [i for i in AddCart.objects.filter(user=user)][-1].order
                    product_order = AddCart(user=user, product=product, gst_value=gst_value, total=total,
                                            per_product_price=product.selling_price,
                                            delivery_charges=product.delivery_charges,
                                            total_after_tax=total_after_tax, order=order_id, status=status)
                    product_order.save()
                else:
                    rendom_id = randint(10**(8-1), (10**8)-1)
                    if not OrderId.objects.filter(order_id=rendom_id).exists():
                        OrderId(order_id=rendom_id).save()
                        product_order = AddCart(user=user, product=product, gst_value=gst_value, total=total,
                                                per_product_price=product.selling_price,
                                                delivery_charges=product.delivery_charges,
                                                total_after_tax=total_after_tax, order=OrderId.objects.last(),
                                                status=status)
                        product_order.save()
        product_order = AddCart.objects.filter(user=user)
        product_order_list = []
        for i in product_order:
            j = model_to_dict(i)
            if i.order:
                j['order'] = str(i.order.order_id)
            if i.user:
                j['user'] = str(i.user.id)
            if i.product:
                j['product'] = product_data_json(i.product)
            for k in j:
                if j[k] is None:
                    j[k] = ''
            product_order_list.append(j)
        return_json['valid'] = True
        return_json['message'] = "Successfully get all Card data"
        return_json['count_result'] = 1
        return_json['data'] = product_order_list
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
@decorator_from_middleware(RemoveCartMiddleware)
def remove_cart_view(request, form=None):
    if request.method == "POST":
        user = Register.objects.get(account_id=request.COOKIES['id'])
        order_id = form.cleaned_data["order_id"]
        product_id = form.cleaned_data["product_id"]
        order_id_obj = OrderId.objects.get(order_id=order_id)
        if AddCart.objects.filter(user=user, order=order_id_obj, product=product_id).exists():
            card_data = AddCart.objects.get(user=user, order=order_id_obj, product=product_id)
            card_data.delete()
            product_order = AddCart.objects.filter(user=user)
            product_order_list = []
            for i in product_order:
                j = model_to_dict(i)
                if i.order:
                    j['order'] = str(i.order.order_id)
                if i.user:
                    j['user'] = str(i.user.id)
                if i.product:
                    j['product'] = product_data_json(i.product)
                for k in j:
                    if j[k] is None:
                        j[k] = ''
                product_order_list.append(j)
            return_json['valid'] = True
            return_json['message'] = "Successfully Remove product from Card data"
            return_json['count_result'] = 1
            return_json['data'] = product_order_list
            return JsonResponse(return_json, safe=False, status=200)


@api_view(['GET', 'POST'])
@decorator_from_middleware(UserCategoryListMiddleware)
def user_category_list_view(request, form):
    if request.method == "POST":
        category_list = form.cleaned_data.get("category_list")
        user_category_list = []
        for i in category_list:
            user_category_list.append(Category.objects.get(id=i).id)
        user = Register.objects.get(account_id=request.COOKIES['id'])
        if UserCategory.objects.filter(user=user).exists():
            category = UserCategory.objects.get(user=user)
            category.list_category = user_category_list
            category.save()
        else:
            category = UserCategory(list_category=user_category_list, user=user)
            category.save()
        return_json['valid'] = True
        return_json['message'] = "Successfully get user Selected Category List"
        return_json['count_result'] = 1
        return_json['data'] = category_list
        return JsonResponse(return_json, status=200, safe=False)
