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
