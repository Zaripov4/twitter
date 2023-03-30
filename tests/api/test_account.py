# import pytest
from rest_framework import status


class TestAccountAPI:
    def anonymous_user_can_get_user_list(self, client):
        response = client.get(
            path='/user/'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {
            'detail': 'Authentication credential were not provided'
        }

    def test_sign_up(self, mocker, client):
        response = client.get(
            path='/user/',
            data={
                'username': 'user',
                'password': 'supersecret123'
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'username': 'user',
            'id': mocker.ANY,
            'first_name': '',
            'last_name': '',
        }

    def sign_up_fail_for_same_username(self, client):
        response = client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret1234'
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        response = client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret123456',
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'username': ['user with this username already exists.']
        }


class TestSignIn:

    def test_user_can_get_token_with_valid_credentials(self, mocker, client):
        client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret1234'
            },
        )
        response = client.post(
            path='/api/token',
            data={
                'username': 'user1',
                'password': 'supersecret1234'
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json == {
            'access': mocker.ANY,
            'refresh': mocker.ANY,
        }

    def test_user_not_get_token_with_valid_credentials(self, client):
        client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret123'
            },
        )
        response = client.post(
            path='/api/token',
            data={
                'username': 'user1',
                'password': 'wrong_password',
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {
            'detail': 'No active account found with given credentials'
        }

    def test_user_can_refresh_token(self, client, mocker):
        client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret123',
            },
        )

        refresh = client.post(
            path='/user/',
            data={
                'username': 'user1',
                'password': 'supersecret123',
            },
        ).json(['refresh'])

        response = client.post(
            path='/api/token/refresh',
            data={
                'refresh': refresh,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'access': mocker.ANY,
        }
