from authy.api import AuthyApiClient
from django.conf import settings
from .admininfo import *

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


def token_sms(phone_number):
    sms = authy_api.phones.verification_start(phone_number, "+91", via="sms")
    if sms.ok():
        return_json['valid'] = True
        return_json['message'] = "SMS request successful"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json
    else:
        return_json['valid'] = False
        return_json['message'] = "SMS request failed"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json


def verify(phone_number, token):
    verification = authy_api.phones.verification_check(phone_number, "+91", token)
    if verification.ok():
        return_json['valid'] = True
        return_json['message'] = "SMS request successfully verify"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json
    else:
        return_json['valid'] = False
        return_json['message'] = "SMS request failed verification"
        return_json['count_result'] = 1
        return_json['data'] = None
        return return_json
