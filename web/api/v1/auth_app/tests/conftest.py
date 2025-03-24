from unittest import mock
from unittest.mock import patch

import pytest

from api.v1.auth_app.services import PasswordResetGenerator


@pytest.fixture()
def inactive_user(user):
    user.is_active = False

    user.save(update_fields=['is_active'])

    return user


@pytest.fixture()
def user_uid_token(user):
    generator = PasswordResetGenerator().encode(user)

    return {'uid': generator.uid, 'token': generator.token}

@pytest.fixture()
def mock_recaptcha():
    with patch('main.mixins.validate_recaptcha', return_value={ 'success': True }) as m:
        yield m

@pytest.fixture()
def mock_recaptcha_fail():
    with patch('main.mixins.validate_recaptcha', return_value={ 'success': False, 'error-codes': 1 }) as m:
        yield m
