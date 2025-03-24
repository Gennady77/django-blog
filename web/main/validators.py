import json
from urllib.parse import urlencode
from urllib.request import urlopen
import requests

from rest_framework import serializers


def validate_recaptcha(token):
    URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'

    params = {
        'secret': '6Ld22e4qAAAAAFeqw3bsmJ7rZReUQp3MQtiwuEtY',
        'response': token,
    }

    response = requests.post(URIReCaptcha, data=params)

    return response.json()
