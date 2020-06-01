from django.db import models
from random import randint


class State(models.Model):
    state_name = models.CharField(max_length=200,  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "State"


class City(models.Model):
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=200,  null=True)
    city_image = models.ImageField(upload_to="user/city/", default='user/city/jaipur.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "City"


class Role(models.Model):
    role_name = models.CharField(max_length=100, null=False, default='User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Role"


class Gender(models.Model):
    Gender_name = models.CharField(max_length=50, null=False, default='Male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Gender"


class DocumentType(models.Model):
    document_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "DocumentType"


class BusinessType(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Register(models.Model):
    password = models.CharField(max_length=200, null=True)
    last_login = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=100,  null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100,  null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=15,  null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    user_profile_img = models.ImageField(upload_to="user/profile/", default='user_default_img.jpg')
    updated_at = models.DateField(auto_now_add=True)
    account_id = models.CharField(max_length=20,  default=randint(10**(8-1), (10**8)-1))
    key = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=2000, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    gst_number = models.CharField(max_length=200, null=True, blank=True)
    token = models.TextField(max_length=2000, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    varification_document_front = models.ImageField(upload_to="user/documents/", null=True, blank=True)
    varification_document_back = models.ImageField(upload_to="user/documents/", null=True, blank=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.PROTECT, null=True, blank=True)
    business_name = models.TextField(max_length=2000, null=True, blank=True)
    business_description = models.TextField(max_length=15000, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=13, blank=True)
    authy_id = models.CharField(max_length=12, null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Register"


class SMTPDetailModel(models.Model):
    smtp_host = models.CharField(max_length=200)
    smtp_email = models.CharField(max_length=200)
    smtp_password = models.TextField(max_length=2000)
    smtp_port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SMTPDetailModel"
