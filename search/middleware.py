from django.utils.deprecation import MiddlewareMixin
from electonicswebservice.admininfo import *
from django.http import HttpResponse, JsonResponse
from .forms import *


class EnquiryFormMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = EnquiryFormForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form)

    def process_template_response(self, request, response):
        return response


class SearchMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = SearchForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    return_json['valid'] = False
                    return_json['message'] = eval(form.errors.as_json())
                    return_json['count_result'] = 1
                    return_json['data'] = None
                    logger.error(form.errors)
                    return JsonResponse(return_json, status=200)
            else:
                return view_func(request, form)

    def process_template_response(self, request, response):
        return response