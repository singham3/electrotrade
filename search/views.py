from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from .models import *
from django.core.paginator import Paginator
from electonicswebservice.admininfo import *
from .forms import *
from products.models import *
from .middleware import *
from products.json_products import *


@api_view(['GET', 'POST'])
@decorator_from_middleware(SearchMiddleware)
def search_view(request, form=None, page=1):
    try:
        if request.method == 'POST':
            search = form.cleaned_data['search']
            user = Register.objects.get(account_id=request.COOKIES['id'])
            search_result_status = True
            if Category.objects.filter(title=search).exists():
                category_data = Category.objects.get(title=search)
                search_result = Products.objects.filter(category=category_data)
                search_result_count = search_result.count()

            elif Brand.objects.filter(name=search).exists():
                product_brand = Brand.objects.get(name=search)
                search_result = Products.objects.filter(brand=product_brand)
                search_result_count = search_result.count()

            elif ProductFilter.objects.filter(filter_value=search).exists():
                search_result = Products.objects.raw(f'''select products.* from 
                                                         electronic_db.products_productfilter as filter
                                                         inner join electronic_db.products_products as products
                                                         on filter.product_id = products.id
                                                         where filter.filter_value = '{search}';''')
                search_result_count = len(list(search_result))

            elif Products.objects.filter(title=search).exists():
                search_result = Products.objects.filter(title=search)
                search_result_count = search_result.count()

            elif Products.objects.filter(model_number=search).exists():
                search_result = Products.objects.filter(model_number=search)
                search_result_count = search_result.count()

            elif Products.objects.filter(serial_number=search).exists():
                search_result = Products.objects.filter(serial_number=search)
                search_result_count = search_result.count()

            else:
                search_result = None
                search_result_status = False
                search_result_count = 0

            if search_result:
                paginator = Paginator(search_result, 10)
                contacts = paginator.get_page(page)
                if contacts is not None:
                    product_data_list = []
                    for i in contacts:
                        j = product_data_json(i)
                        product_data_list.append(j)
                    return_json['valid'] = True
                    return_json['message'] = "Successfully get all brand data"
                    return_json['count_result'] = 1
                    return_json['data'] = product_data_list
            else:
                return_json['valid'] = False
                return_json['message'] = "search key not found in database"
                return_json['count_result'] = 0
                return_json['data'] = "No result search found"

            if Search.objects.filter(search=search).exists():
                search_obj = Search.objects.get(search=search)
                search_obj.search_count += 1
                search_obj.search_result_status = search_result_status
                search_obj.search_result_count = search_result_count
                search_obj.updated_at = datetime.now()
                search_obj.save()
            else:
                search_obj = Search(user_id=user, search=search, search_result_status=search_result_status,
                                    search_result_count=search_result_count, search_count=1)
                search_obj.save()
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
@decorator_from_middleware(EnquiryFormMiddleware)
def enquiry_form_view(request, form):
    try:
        if request.method == 'POST':
            enquiry_form_data = EnquiryForm(user=Register.objects.get(account_id=request.COOKIES['id']),
                                            product_name=form.cleaned_data['product_name'],
                                            product_company=form.cleaned_data['product_company'],
                                            product_series_num=form.cleaned_data['product_series_num'],
                                            prod_description=form.cleaned_data['prod_description'])
            enquiry_form_data.save()

            return_json['valid'] = True
            return_json['message'] = "Successfully save Enquiry Form data"
            return_json['count_result'] = 1
            return_json['data'] = "Thank you for your Enquiry, we get your product as soon as."
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

