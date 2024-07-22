from time import sleep
from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from rag_backend import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from urllib.parse import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from .serializers import SignInSerializer
from rest_framework.permissions import IsAuthenticated
from rag_backend import settings


def send_confirmation_mail(user, request):
    messages.success(
        request, 'Your account has been successfully created.We have send you confirmation email, please confirm your email in order to activate your account')
    # Welcome message using email
    subject = "Welcome to Quiz generator"
    message = "Hello " + \
        f"{user.first_name} ! \n Welcome to Quiz generator \n We have also sent you a confirmation email, please confirm your email "
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    send_mail(subject, message, from_email,
              to_list, fail_silently=True)

    # # Confirmation email
    # current_site = settings.FRONTEND_URL
    # email_subject = "Confirm your email @Quiz Generator"
    # message2 = render_to_string(
    #     {'name': user.first_name,
    #      'domain': 5173,
    #      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #      'token': generate_token.make_token(user), })
    # email = EmailMessage(
    #     email_subject,
    #     message2,
    #     settings.EMAIL_HOST_USER,
    #     [user.email],
    # )
    # email.fail_silently = True
    # email.send()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)
    confirmation_url = (
        f"{settings.FRONTEND_URL}/authentication/api/email-verify?"
        f"{urlencode({'uid': uid, 'token': token})}"
    )
    user.email_verification_token = token
    user.save()
    # Send the confirmation URL in the email
    subject = 'Confirm your email'
    message = (
        f"Hello {user.first_name},\n\nPlease confirm your email by clicking the link "
        f"below:\n{confirmation_url}"
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    send_mail(subject, message, from_email, [to_email], fail_silently=True)
    # return redirect(settings.FRONTEND_URL + '/home')


class SignUpView(APIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            send_confirmation_mail(user, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)
    def post(self, request, format=None):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'User is not active'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def post(self, request, format=None):
#        serializer = SignInSerializer(data=request.data)
#        if serializer.is_valid():
#            username = serializer.data['username']
#            password = serializer.data['password']

#           user = authenticate(username=username, password=password)
#           if user is not None:
#                if user.is_active:
#                    token, _ = Token.objects.get_or_create(user=user)
#                    return Response({'token': token.key}, status=status.HTTP_200_OK)
#                else:
#                    return Response({'error': 'User is not active, please verify email'}, status=status.HTTP_400_BAD_REQUEST)
#            else:
#                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#        else:
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # def get(self, request, format=None):
#        if request.user.is_authenticated:
 #           logout(request)
#       request.user.auth_token.delete()
     #   return Response(status=status.HTTP_204_NO_CONTENT)
#        else:
#            return Response({'detail': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)

    def get(self, request, format=None):
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid confirmation link'}, status=status.HTTP_400_BAD_REQUEST)

        stored_token = user.email_verification_token

        if stored_token != token:
            return Response({'detail': 'Invalid confirmation link'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        login(request, user)
        return Response({'detail': 'Email confirmed successfully'}, status=status.HTTP_200_OK)
