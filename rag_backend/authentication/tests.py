from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import generate_token
from urllib.parse import urlencode


class TestSignUpView(APITestCase):
    def test_post_method(self):
        data = {
            "username": "test",
            "email": "johndoe@gmail.com",
            "first_name": "test",
            "last_name": "test",
            "telegram_id": "test",
            "password": "test",
        }
        response = self.client.post(
            "/authentication/api/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestSignInView(APITestCase):
    def test_post_method(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.is_active = True
        user.save()

        data = {"username": "test", "password": "test"}
        response = self.client.post(
            "/authentication/api/signin/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSignOutView(APITestCase):
    def test_get_method(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.is_active = True
        user.save()

        self.client.force_login(user)
        response = self.client.get("/authentication/api/signout/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestConfirmEmalAPIView(APITestCase):
    def test_get_method(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)

        user.email_verification_token = token
        user.save()

        response = self.client.get(
            f"/authentication/api/email-verify?{urlencode({"uid": uid, "token": token})}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
