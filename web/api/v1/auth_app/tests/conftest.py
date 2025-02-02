import pytest

@pytest.fixture()
def inactive_user(user):
    user.is_active = False

    user.save(update_fields=['is_active'])

    return user
