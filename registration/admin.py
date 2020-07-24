from django.conf.urls import url
from django.contrib import admin
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse
from .services import *
from django.forms.models import model_to_dict
from electonicswebservice.hashers import *
from django.contrib import messages
import json
from django.contrib import messages


class RegisterAdminView(admin.ModelAdmin):
    def role_name(self, obj):
        if obj is not None:
            return obj.role.role_name
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'mobile',  'role_name', 'account_id', 'user_profile_img',
                    'status', 'date_joined')
    form = RegisterForm

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            # form = RegisterForm(request.POST, request.FILES)
            if not form.is_valid():
                if form.errors:
                    return_json['message'] = eval(form.errors.as_json())
                    return JsonResponse(return_json, status=200)
            else:
                new_user = CreateUserService.execute({
                    'password': form.cleaned_data.get('password'),
                    'username': form.cleaned_data.get('username'),
                    'first_name': form.cleaned_data.get('first_name'),
                    'last_name': form.cleaned_data.get('last_name'),
                    'email': form.cleaned_data.get('email'),
                    'gender': form.cleaned_data.get('gender').id if form.cleaned_data.get('gender') else None,
                    'role': form.cleaned_data.get('role').id if form.cleaned_data.get('role') else None,
                    'is_active': form.cleaned_data.get('is_active'),
                    'mobile': form.cleaned_data.get('mobile'),
                    'date_of_birth': form.cleaned_data.get('date_of_birth'),
                    'account_id': form.cleaned_data.get('account_id'),
                    'city': form.cleaned_data.get('city').id if form.cleaned_data.get('city') else None,
                    'state': form.cleaned_data.get('state').id if form.cleaned_data.get('state') else None,
                    'address': form.cleaned_data.get('address'),
                    'pincode': form.cleaned_data.get('pincode'),
                    'gst_number': form.cleaned_data.get('gst_number'),
                    'document_type': form.cleaned_data.get('document_type').id if form.cleaned_data.get('document_type') else None,
                    'business_type': form.cleaned_data.get('business_type').id if form.cleaned_data.get('business_type') else None,
                    'business_name': form.cleaned_data.get('business_name'),
                    'business_description': form.cleaned_data.get('business_description'),
                    'alternate_mobile': form.cleaned_data.get('alternate_mobile'),
                    'status': True if form.cleaned_data.get('status') else None,
                }, {'user_profile_img': form.cleaned_data.get('user_profile_img'),
                    'varification_document_front': form.cleaned_data.get('varification_document_front'),
                    'varification_document_back': form.cleaned_data.get('varification_document_back'),
                    })
                if isinstance(new_user, str):
                    messages.error(request, new_user)
                else:
                    messages.info(request, "User Successfully Created")


class GenderAdminView(admin.ModelAdmin):
    list_display = ('id', 'Gender_name', 'created_at')


class StateAdminView(admin.ModelAdmin):
    list_display = ('id', 'state_name', 'created_at')


class CityAdminView(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'state_id':
            return StateChoiceField(queryset=State.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def state_name(self, obj):
        return obj.state_id.state_name
    list_display = ('id', 'city_name', 'state_name', 'city_image', 'created_at')


class RoleAdminView(admin.ModelAdmin):
    list_display = ('id', 'role_name', 'created_at')


class DocumentTypeAdminView(admin.ModelAdmin):
    list_display = ('id', 'document_name', 'created_at')


class SMTPDetailModelAdminView(admin.ModelAdmin):
    list_display = ('id', 'created_at')

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            try:
                smtp_host = request.POST.get('smtp_host')
                smtp_email = request.POST.get('smtp_email')
                smtp_password = encrypt_message_rsa(request.POST.get('smtp_password'), public_key)
                smtp_port = int(request.POST.get('smtp_port'))
                if SMTPDetailModel.objects.filter().exists():
                    smtp_obj = SMTPDetailModel.objects.get()
                    smtp_obj.smtp_host = smtp_host
                    smtp_obj.smtp_email = smtp_email
                    smtp_obj.smtp_password = smtp_password
                    smtp_obj.smtp_port = smtp_port
                    smtp_obj.updated_at = datetime.now()
                    smtp_obj.save()
                else:
                    SMTPDetailModel(smtp_host=smtp_host, smtp_email=smtp_email, smtp_password=smtp_password,
                                    smtp_port=smtp_port).save()
                messages.info(request, "Successfully Update SMTP Details", )
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
                messages.error(request, f"{e}, {f_name}, {exc_tb.tb_lineno}")


class BusinessTypeAdminView(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')


admin.site.register(Register, RegisterAdminView)
admin.site.register(State, StateAdminView)
admin.site.register(City, CityAdminView)
admin.site.register(Role, RoleAdminView)
admin.site.register(Gender, GenderAdminView)
admin.site.register(DocumentType, DocumentTypeAdminView)
admin.site.register(SMTPDetailModel, SMTPDetailModelAdminView)
admin.site.register(BusinessType, BusinessTypeAdminView)
