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
from django.utils import timezone


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
def user_reward_view(request):
    try:
        user = Register.objects.get(account_id=request.COOKIES['id'])
        if ProductReward.objects.filter(user=user).exists():
            reward = product_reward_json(ProductReward.objects.get(user=user))
        else:
            ProductReward(user=user, reward_point=0.0).save()
            reward = product_reward_json(ProductReward.objects.get(user=user))
        return_json['valid'] = True
        return_json['message'] = "Successfully get User Reward Data"
        return_json['count_result'] = 1
        return_json['data'] = reward
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
            method = None
            if ProductsPaymentMethod.objects.filter(method=payment_method).exists():
                if payment_method == "COD":
                    payment_status = "Unpaid"
                method = ProductsPaymentMethod.objects.get(method=payment_method)
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
                delivery_date_time = datetime.now() + timedelta(days=order.product.delivery_days)
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
                    order_product.delivery_date_time = delivery_date_time
                    if order.product.is_replacement:
                        order_product.replacement_from = datetime.now()
                        order_product.replacement_to = datetime.now() + relativedelta(months=+order.product.replacement_duration)
                    order_product.save()
                    product_order = OrderProduct.objects.get(user=user, order=order.order, product=order.product)
                else:
                    OrderProduct(user=user, order=order.order, product=order.product, price=price, quantity=quantity,
                                 gst_per=gst_per, total_after_tax=total_after_tax,
                                 delivery_days=order.product.delivery_days,
                                 delivery_date_time=delivery_date_time,
                                 delivery_charges=order.product.delivery_charges,
                                 is_replacement=order.product.is_replacement,
                                 replacement_from=datetime.now() if order.product.is_replacement else None,
                                 replacement_to=datetime.now() + relativedelta(months=+order.product.replacement_duration) if order.product.is_replacement else None,
                                 delivery_address=order_address
                                 ).save()
                    product_order = OrderProduct.objects.last()
                OrderProductDeliver(user=user, order=order.order, product=order.product,
                                    order_product=product_order, product_price=total_after_tax,
                                    payment_status=payment_status, payment_method=method,
                                    delivery_date_time=delivery_date_time).save()
                AddCart.objects.get(id=order.id).delete()
                order = product_order.order
                all_product_price += total_after_tax
            if ProductsPaymentMethod.objects.filter(method=payment_method).exists():
                if payment_method == "COD":
                    payment_status = "Unpaid"
                    if reward_point:
                        if reward_point.reward_point >= 1000.0:
                            total_products_price = all_product_price - 1000.0
                            reward_point.reward_point = reward_point.reward_point - 1000.0
                            reward_point.save()
                        else:
                            total_products_price = all_product_price - reward_point.reward_point
                            reward_point.reward_point = 0.0
                            reward_point.save()
                        RewardRedeem(user=user, points=reward_point.reward_point, order=order).save()
                    else:
                        total_products_price = all_product_price
                mehtod = ProductsPaymentMethod.objects.get(method=payment_method)
                ProductPayments(user=user, order=order, total_after_tax=all_product_price,
                                reward=reward_point, payment_method=mehtod, payment_status=payment_status,
                                total_products_price=total_products_price).save()
                product_order_list['ProductPayments'] = product_payments_json(ProductPayments.objects.last())
                if ProductReward.objects.filter(user=user).exists():
                    product_order_list['ProductReward'] = product_reward_json(ProductReward.objects.get(user=user))
                else:
                    ProductReward(user=user, reward_point=0.0).save()
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


@api_view(['GET', 'POST'])
@decorator_from_middleware(OrderProductCancelMiddleware)
def order_product_cancel_view(request, form=None):
    try:
        user = Register.objects.get(account_id=request.COOKIES['id'])
        if request.method == "POST":
            order = OrderId.objects.get(order_id=form.cleaned_data['order_id'])
            product = Products.objects.get(id=form.cleaned_data['product_id'])
            cancellation_description = None
            if 'cancellation_description' in form.cleaned_data:
                cancellation_description = form.cleaned_data['cancellation_description']
            product_payments = ProductPayments.objects.get(user=user, order=order, is_cancel=False)
            order_product = OrderProduct.objects.get(user=user, product=product, order=order, is_cancel=False)
            if OrderProductDeliver.objects.filter(user=user, product=product, order=order, order_product=order_product, payment_status='Unpaid', is_delivered=False).exists():
                if order_product.delivery_date_time > timezone.now():
                    order_product.is_delivered = False
                    order_product.is_cancel = True
                    order_product.delivery_status = 'Product cancelled'
                    order_product.order_cancel_date_time = datetime.now()
                    order_product.delivery_charges = None
                    order_product.cancellation_description = cancellation_description
                    order_product.updated_at = datetime.now()
                    order_product.save()
                    product_payments.total_products_price = product_payments.total_products_price - order_product.total_after_tax
                    product_payments.created_at = datetime.now()
                    product_payments.save()
                    OrderProductDeliver.objects.get(user=user, product=product, order=order,
                                                    order_product=order_product).delete()
            if not OrderProduct.objects.filter(user=user, order=order, is_cancel=False).exists():
                product_payments = ProductPayments.objects.get(user=user, order=order, is_cancel=False)
                product_payments.is_cancel = True
                product_payments.payment_status = 'Order cancelled'
                product_payments.save()
                if RewardRedeem.objects.filter(user=user, order=order).exists():
                    reward_redeem = RewardRedeem.objects.get(user=user, order=order)
                    reward = ProductReward.objects.get(user=user)
                    reward.reward_point += reward_redeem.points
                    reward.updated_at = datetime.now()
                    reward.save()
                    reward_redeem.delete()
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
                if k.created_at:
                    j['created_at'] = str(k.created_at.strftime("%Y/%m/%d %H:%M:%S"))
                if k.delivery_charges is None:
                    j['delivery_charges'] = 0.0
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
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return_json['valid'] = False
        return_json['message'] = f"{e}, {f_name}, {exc_tb.tb_lineno}"
        return_json['count_result'] = 1
        return_json['data'] = None
        return JsonResponse(return_json, status=200, safe=False)
