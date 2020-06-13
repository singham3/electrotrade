from django import forms
from .models import *
from electonicswebservice.admininfo import *
from django.forms import BaseModelForm, ModelForm


class StateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.state_name)


class CityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.city_name)


class RoleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.role_name)


class GenderChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.Gender_name)


class DocumentTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.document_name)


class BusinessTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.title)


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(required=True)
    gender = GenderChoiceField(queryset=Gender.objects.all(), required=False)
    role = RoleChoiceField(queryset=Role.objects.all(), required=False)
    user_profile_img = forms.ImageField(required=False)
    account_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                 initial=randint(10**(8-1), (10**8)-1))
    city = CityChoiceField(queryset=City.objects.all(), required=False)
    state = StateChoiceField(queryset=State.objects.all(), required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    pincode = forms.CharField(required=False)
    gst_number = forms.CharField(required=False)
    document_type = DocumentTypeChoiceField(queryset=DocumentType.objects.all(), required=False)
    varification_document_front = forms.FileField(required=False)
    varification_document_back = forms.FileField(required=False)
    is_active = forms.BooleanField(required=False)
    status = forms.BooleanField(required=False)
    business_type = BusinessTypeChoiceField(queryset=BusinessType.objects.all(), required=False)
    business_name = forms.CharField(widget=forms.Textarea, required=False)
    business_description = forms.CharField(widget=forms.Textarea, required=False)
    alternate_mobile = forms.CharField(required=False)

    class Meta:
        model = Register
        fields = ('username', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'user_profile_img', 'gender',
                  'role', 'email', 'city', 'state', 'address', 'pincode', 'gst_number', 'account_id',
                  'varification_document_front', 'varification_document_back', 'document_type', 'business_type',
                  'business_name', 'business_description', 'alternate_mobile', 'is_active', 'status',
                  'password')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        account_id = cleaned_data.get("account_id")
        mobile = cleaned_data.get("mobile")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if Register.objects.filter(username=username, account_id=account_id).exists():
            return cleaned_data
        else:
            if Register.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists !!!!!!")
            if Register.objects.filter(username=username).exists():
                raise forms.ValidationError("username already exists !!!!!!")
            if Register.objects.filter(mobile=mobile).exists():
                raise forms.ValidationError("mobile already exists !!!!!!")
            if Register.objects.filter(account_id=account_id).exists():
                raise forms.ValidationError("Account Id already exists !!!!!!")
            if password is None or password == '':
                raise forms.ValidationError("password field is required")


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = Register
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        if not Register.objects.filter(username=username).exists():
            raise forms.ValidationError("User is not Valid")
        else:
            return cleaned_data


class ForgetPassForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = Register
        fields = ('email', )

    def clean(self):
        cleaned_data = super(ForgetPassForm, self).clean()
        email = cleaned_data.get("email")

        if not Register.objects.filter(email=email).exists():
            raise forms.ValidationError(
               ugettext("This email address does not exist in database.!")
            )
        else:
            return cleaned_data


class ForgetPasswordForm(forms.Form):
    confirm_password = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = Register
        fields = ('password', 'confirm_password')

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password != password:
            raise forms.ValidationError(
               ugettext("Password And Confirm Password Not Match")
            )
        else:
            return cleaned_data


class UserProfileEditForm(forms.Form):
    business_type = forms.CharField(required=False)
    business_name = forms.CharField(required=False)
    alternate_mobile = forms.CharField(required=False)
    business_description = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    address = forms.CharField(required=False)
    pincode = forms.CharField(required=False)
    user_profile_img = forms.FileField(required=False)

    class Meta:
        model = Register
        fields = ('user_profile_img', 'business_type', 'business_name', 'alternate_mobile', 'city', 'state', 'address', 'pincode',
                  'business_description')

    def clean(self):
        cleaned_data = super(UserProfileEditForm, self).clean()
        return cleaned_data
