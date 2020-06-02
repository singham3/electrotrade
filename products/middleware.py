from django.utils.deprecation import MiddlewareMixin
from electonicswebservice.admininfo import *
from django.http import HttpResponse, JsonResponse
from .forms import *
from .json_products import *


class ProductReviewMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = ProductReviewForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form=form)
        else:
            if 'id' in view_kwargs:
                return view_func(request, view_kwargs['id'])

    def process_template_response(self, request, response):
        return response


class OrderMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = OrderForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    error = eval(form.errors.as_json())
                    if '__all__' in error:
                        error = eval(error['__all__'][0]['message'])[0]
                    return_json['valid'] = False
                    return_json['message'] = error
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form=form)
        else:
            return None

    def process_template_response(self, request, response):
        return response


class ProductOrderMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = ProductOrderForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form=form)
        else:
            user = Register.objects.get(account_id=request.COOKIES['id'])
            product_payments = ProductPayments.objects.filter(user=user)
            product_order_dict = []
            for i in product_payments:
                product_order_list = []
                product_order = OrderProduct.objects.filter(user=user, order=i.order)
                for k in product_order:
                    j = model_to_dict(k)
                    if k.user:
                        j['user'] = str(k.user.id)
                    if k.order:
                        j['order'] = str(k.order.order_id)
                    if k.product:
                        j['product'] = product_data_json(k.product)
                    for m in j:
                        if j[m] is None:
                            j[m] = ''
                    product_order_list.append(j)
                product_reward = product_reward_json(ProductReward.objects.get(user=user))
                product_payment = product_payments_json(i)
                product_payment['product_order'] = product_order_list
                product_payment['product_reward'] = product_reward
                product_order_dict.append(product_payment)
            return_json['valid'] = True
            return_json['message'] = "Successfully get all Order Product data"
            return_json['count_result'] = 1
            return_json['data'] = product_order_dict
            return JsonResponse(return_json, safe=False, status=200)

    def process_template_response(self, request, response):
        return response


class UserCategoryListMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = UserCategoryForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form=form)
        else:
            user = Register.objects.get(account_id=request.COOKIES['id'])
            category_list = []
            if UserCategory.objects.filter(user=user).exists():
                category = UserCategory.objects.get(user=user)
                category_list = category.list_category
            return_json['valid'] = True
            return_json['message'] = "Successfully get all Product Order Address data"
            return_json['count_result'] = 1
            return_json['data'] = category_list
            return JsonResponse(return_json, status=200, safe=False)

    def process_template_response(self, request, response):
        return response


class RemoveCartMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = RemoveCartForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form=form)

    def process_template_response(self, request, response):
        return response


