import json
from urllib.parse import urlencode
from urllib.request import urlopen
import requests
from django.conf import settings

from rest_framework import serializers


def validate_recaptcha(token):
    URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'

    params = {
        'secret': settings.G_RECAPTCHA_SECRET_KEY,
        'response': token,
    }

    response = requests.post(URIReCaptcha, data=params)

    return response.json()
