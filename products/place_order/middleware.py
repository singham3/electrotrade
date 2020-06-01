from django.utils.deprecation import MiddlewareMixin
from electonicswebservice.admininfo import *
from django.http import HttpResponse, JsonResponse
from .forms import *
from products.json_products import *


class ProductOrderAddressMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = ProductOrderAddressForm(request.POST)
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
            order_address = order_address_data_json(OrderAddress.objects.filter(user=user, is_active=True))
            return_json['valid'] = True
            return_json['message'] = "Successfully get all Product Order Address data"
            return_json['count_result'] = 1
            return_json['data'] = order_address
            return JsonResponse(return_json, safe=False, status=200)

    def process_template_response(self, request, response):
        return response


class ProductOrderSelectAddressMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = ProductOrderSelectAddressForm(request.POST)
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
            return None

    def process_template_response(self, request, response):
        return response