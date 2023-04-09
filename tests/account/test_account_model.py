import pytest
from rest_framework.validators import ValidationError

from blog.models import User

pytestmark = pytest.mark.django_db

USER_PAYLOAD = {
    "username": "joe",
    "email": "joe@gmail.com",
    "password": "supersecret",
}


class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(**USER_PAYLOAD)

        assert user
        assert user.username == USER_PAYLOAD["username"]
        assert user.email == USER_PAYLOAD["email"]
        assert user.check_password(USER_PAYLOAD["password"])

    def test_create_super_user(self):
        user = User.objects.create_super_user(**USER_PAYLOAD)

        assert user
        assert user.username == USER_PAYLOAD["username"]
        assert user.email == USER_PAYLOAD["email"]
        assert user.is_staff
        assert user.is_superuser
        assert user.check_password(USER_PAYLOAD["password"])

    @pytest.mark.parametrize(
        "username, password, email",
        [
            (None, None, None),
            ("joe", None, None),
            ("joe", "supersecret", None),
            ("joe", None, "joe@gmail.com"),
            (None, "supersecret", None),
            (None, "supersecret", "joe@gmail.com"),
            ("joe", "supersecret", None),
            (None, None, "joe@gmail.com"),
            (None, "supersecret", "joe@gmail.com"),
            ("joe", None, "joe@gmail.com"),
            ("joe", "supersecret", "joe@gmail.com"),
        ],
    )
    def test_invalid_data_does_not_create_user(self, username, password, emial):
        with pytest.raises(ValidationError):
            User.objects.create_user(username=username, password=password, emial=emial)
        assert User.objects.count() == 0

    def test_create_user_with_same_username_fails(self):
        User.objects.create_user(**USER_PAYLOAD)
        with pytest.raises(ValidationError) as exc:
            User.objects.create_user(
                username="joe", password="supersecret1234", email="joe@gmail.com"
            )
        assert exc.value.messages == ["User with this username already exists"]
        assert User.objects.count() == 1

    def test_create_user_with_same_email_fails(self):
        User.objects.create_user(**USER_PAYLOAD)
        with pytest.raises(ValidationError) as exc:
            User.objects.create_user(
                username="alex", password="something", email="joe@gmail.com"
            )
        assert exc.value.message == ["User with this email already exists"]
        assert User.objects.count() == 1
