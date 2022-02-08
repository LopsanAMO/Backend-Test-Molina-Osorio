from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class TestLoginView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}

    def test_login_credentials_ok(self):
        response = self.client.post(self.url_login, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        verification_url = reverse("token_verify")
        resp = self.client.post(verification_url, {"token": token}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_login_credentails_fail(self):
        payload = {"username": "foo2", "password": "p"}
        response = self.client.post(self.url_login, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_not_active_account_credentials(self):
        user = User.objects.create_user(
            username="foo4", email="user@foo.com", password="pass", is_active=False
        )
        payload = {"username": "foo4", "password": "pass"}
        response = self.client.post(self.url_login, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)