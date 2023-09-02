import random

import requests
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger

from users.models import *


logger = get_task_logger(__name__)

__all__ = [
    'send_otp_sms',
    'test_task',
]


@shared_task
def test_task():
    logger.info('++++++++++++++ test ++++++++++++++')


def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(5))


@shared_task
def send_otp_sms(user_id: str):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    code = generate_otp()
    logger.info(f'sign up code: {user = } {code = }')

    UserOTP.objects.create(user=user, code=code)

    # headers = {
    #     'X-API-KEY': settings.SMS_API_KEY
    # }
    # data = {
    #     'mobile':     user.mobile,
    #     'templateId': settings.SMS_TEMPLATE_ID,
    #     'parameters': [
    #         {
    #             'name':  'code',
    #             'value': str(code)
    #         }
    #     ]
    # }
    # response = requests.post(url=settings.SMS_WEBSERVICE_URL, json=data, headers=headers)
    # data = response.json()
    # if data.get('status') != 1:
    #     logger.error(data)
    # else:
    #     logger.info(data)
