from products.json_products import *
from products.models import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from electonicswebservice.admininfo import *
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from electonicswebservice.otpsend import *
from products.middleware import *
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from django.utils.timezone import localtime


@api_view(['GET', 'POST'])
@decorator_from_middleware(ProductOrderAddressMiddleware)
def product_order_address_view(request, form=None):
    try:
        if request.method == 'POST':
            user = Register.objects.get(account_id=request.COOKIES['id'])
            city = City.objects.get(city_name=form.cleaned_data['city_name'])
            state = State.objects.get(state_name=form.cleaned_data['state_name'])
            mobile_no = None
            if 'mobile_no' in form.cleaned_data:
                mobile_no = form.cleaned_data['mobile_no']
            pincode = form.cleaned_data['pincode']
            address = form.cleaned_data['address']
            OrderAddress(user=user, city=city, state=state, pincode=pincode, address=address, mobile_no=mobile_no).save()
            product_order_address = order_address_data_json(OrderAddress.objects.filter(user=user, is_active=True))
            return_json['valid'] = True
            return_json['message'] = "Successfully get all Product Order Address data"
            return_json['count_result'] = 1
            return_json['data'] = product_order_address
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
@decorator_from_middleware(ProductOrderAddressMiddleware)
def product_order_edit_address_view(request, form=None):
    try:
        if request.method == 'POST':
            city = City.objects.get(city_name=form.cleaned_data['city_name'])
            state = State.objects.get(state_name=form.cleaned_data['state_name'])
            key = None
            if 'address_id' not in form.cleaned_data:
                return_json['valid'] = False
                return_json['message'] = "Product Order Address ID is Required"
                return_json['count_result'] = 0
                return_json['data'] = "Product Order Address ID is Required"
                return JsonResponse(return_json, safe=False, status=200)
            address_id = form.cleaned_data['address_id']
            mobile_no = None
            if 'mobile_no' in form.cleaned_data:
                mobile_no = form.cleaned_data['mobile_no']
            pincode = form.cleaned_data['pincode']
            address = form.cleaned_data['address']
            if OrderAddress.objects.filter(id=int(address_id), is_active=True).exists():
                order_address = OrderAddress.objects.get(id=int(address_id), is_active=True)
                order_address.city = city
                order_address.state = state
                order_address.pincode = pincode
                order_address.address = address
                order_address.mobile_no = mobile_no
                order_address.updated_at = datetime.now()
                order_address.save()
                product_order_address = order_address_data_json(OrderAddress.objects.filter(id=int(address_id),
                                                                                            is_active=True))
                return_json['valid'] = True
                return_json['message'] = "Successfully Update Product Order Address data"
                return_json['count_result'] = 1
                return_json['data'] = product_order_address
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
@decorator_from_middleware(ProductOrderSelectAddressMiddleware)
def product_order_remove_address_view(request, form=None):
    try:
        if request.method == "POST":
            user = Register.objects.get(account_id=request.COOKIES['id'])
            selected_address = int(form.cleaned_data["address_id"])
            if OrderAddress.objects.filter(id=selected_address).exists():
                order_address = OrderAddress.objects.get(id=selected_address)
                order_address.is_active = False
                order_address.save()
                product_order_address = order_address_data_json(OrderAddress.objects.filter(user=user, is_active=True))
                return_json['valid'] = True
                return_json['message'] = "Successfully get all Product Order Address data"
                return_json['count_result'] = 1
                return_json['data'] = product_order_address
            else:
                return_json['valid'] = False
                return_json['message'] = "Order Address id not exists"
                return_json['count_result'] = 0
                return_json['data'] = "Order Address id not exists"
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
@decorator_from_middleware(ProductOrderSelectAddressMiddleware)
def product_order_select_address_view(request, form=None):
    try:
        if request.method == "POST":
            user = Register.objects.get(account_id=request.COOKIES['id'])
            selected_address = form.cleaned_data["address_id"]
            product_order_address = OrderAddress.objects.filter(user=user)
            for i in product_order_address:
                if i.id == int(selected_address):
                    i.status = True
                else:
                    i.status = False
                i.save()
            return_json['valid'] = True
            return_json['message'] = "Selected Address Successfully Active"
            return_json['count_result'] = 1
            return_json['data'] = "Selected Address Successfully Active"
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
def sms_otp_send_view(request):
    try:
        user = Register.objects.get(account_id=request.COOKIES['id'])
        otp_response = token_sms(user.mobile)
        return JsonResponse(otp_response, safe=False, status=200)
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
def sms_otp_verify_view(request):
    try:
        if request.method == "POST":
            user = Register.objects.get(account_id=request.COOKIES['id'])
            otp_response = verify(user.mobile, request.POST.get('otp'))
            return JsonResponse(otp_response, safe=False, status=200)
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
@decorator_from_middleware(ProductOrderMiddleware)
def order_product_view(request, form):
    try:
        if request.method == 'POST':
            user = Register.objects.get(account_id=request.COOKIES['id'])
            order_obj = AddCart.objects.filter(user=user, order=OrderId.objects.get(
                                                                                order_id=form.cleaned_data['order_id']))
            reward = form.cleaned_data['reward']
            payment_method = form.cleaned_data['payment_method']
            payment_status = None
            product_order_list = {}
            all_product_price = 0
            total_products_price = 0
            order = None
            reward_point = None
            if ProductReward.objects.filter(user=user).exists() and reward:
                if ProductReward.objects.get(user=user).reward_point >= 50.0:
                    reward_point = ProductReward.objects.get(user=user)
            order_address = OrderAddress.objects.get(user=user, status=True)
            for order in order_obj:
                price = order.product.selling_price
                delivery_charges = order.product.delivery_charges
                quantity = order.total
                gst_per = order.product.gst_per if order.product.gst_per else 0.0
                total_after_tax = (price*quantity) + delivery_charges
                if order_address.state.state_name != 'Rajsthan':
                    if ProductIGST.objects.filter(product=order.product).exists():
                        total_after_tax = (price*quantity) + ProductIGST.objects.get(product=order.product).igst_value + delivery_charges
                if OrderProduct.objects.filter(user=user, order=order.order, product=order.product).exists():
                    order_product = OrderProduct.objects.get(user=user, order=order.order, product=order.product)
                    order_product.price = price
                    order_product.quantity = quantity
                    order_product.gst_per = gst_per
                    order_product.total_after_tax = total_after_tax
                    order_product.delivery_days = order.product.delivery_days
                    order_product.delivery_charges = order.product.delivery_charges
                    order_product.is_replacement = order.product.is_replacement
                    order_product.delivery_address = order_address
                    order_product.delivery_date_time = datetime.now() + timedelta(days=order.product.delivery_days),
                    if order.product.is_replacement:
                        order_product.replacement_from = datetime.now()
                        order_product.replacement_to = datetime.now() + relativedelta(months=+order.product.replacement_duration)
                    order_product.save()
                    product_order = OrderProduct.objects.get(user=user, order=order.order, product=order.product)
                else:
                    OrderProduct(user=user, order=order.order, product=order.product, price=price, quantity=quantity,
                                 gst_per=gst_per, total_after_tax=total_after_tax,
                                 delivery_days=order.product.delivery_days,
                                 delivery_date_time=datetime.now() + timedelta(days=order.product.delivery_days),
                                 delivery_charges=order.product.delivery_charges,
                                 is_replacement=order.product.is_replacement,
                                 replacement_from=datetime.now() if order.product.is_replacement else None,
                                 replacement_to=datetime.now() + relativedelta(months=+order.product.replacement_duration) if order.product.is_replacement else None,
                                 delivery_address=order_address
                                 ).save()
                    product_order = OrderProduct.objects.last()
                AddCart.objects.get(id=order.id).delete()
                order = product_order.order
                all_product_price += total_after_tax
            if ProductsPaymentMethod.objects.filter(method=payment_method).exists():
                if payment_method == "COD":
                    payment_status = "Unpaid"
                    if reward_point:
                        total_products_price = all_product_price - reward_point.reward_point
                        RewardRedeem(user=user, points=reward_point.reward_point, order=order).save()
                        reward_point.reward_point = 0.0
                        reward_point.save()
                mehtod = ProductsPaymentMethod.objects.get(method=payment_method)
                ProductPayments(user=user, order=order, total_after_tax=all_product_price,
                                reward=reward_point, payment_method=mehtod, payment_status=payment_status,
                                total_products_price=total_products_price).save()
                product_order_list['ProductPayments'] = product_payments_json(ProductPayments.objects.last())
                # for rewards_point in OrderProduct.objects.filter(user=user, order=order):
                #     if ProductReward.objects.filter(user=user, order=order).exists():
                #         product_reward = ProductReward.objects.get(user=user, order=order)
                #         product_reward.reward_point += rewards_point.product.rewards
                #         product_reward.save()
                #     else:
                #         ProductReward(user=user, order=order, reward_point=rewards_point.product.rewards).save()
                if ProductReward.objects.filter(user=user).exists():
                    product_order_list['ProductReward'] = product_reward_json(ProductReward.objects.get(user=user))
                else:
                    ProductReward(user=user, order=order, reward_point=0.0).save()
                    product_order_list['ProductReward'] = product_reward_json(ProductReward.objects.get(user=user))

            return_json['valid'] = True
            return_json['message'] = "Successfully get all Order Product data"
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
