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
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from .serializers import SignInSerializer
from rest_framework.permissions import IsAuthenticated


class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.


class SignInView(APIView):
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


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'authentication/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        telegram_id = request.POST['telegram-id']

        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(telegram_id=telegram_id).exists():
                messages.info(request, 'Telegram ID already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                # hashed_password = make_password(pass1)
                myuser = User.objects.create(username=username, email=email,
                                             password=pass1, first_name=fname, last_name=lname, telegram_id=telegram_id)

                myuser.is_active = False
                myuser.save()
                messages.success(
                    request, 'Your account has been successfully created.We have send you confirmation email, please confirm your email in order to activate your account')

                # Welcome message using email
                subject = "Welcome to Quiz generator"
                message = "Hello " + myuser.first_name + "!! \n" + \
                    "Welcome to Quiz generator \n We have also sent you a confirmation email, please confirm your email "
                from_email = settings.EMAIL_HOST_USER
                to_list = [myuser.email]
                send_mail(subject, message, from_email,
                          to_list, fail_silently=True)

                # Confirmation email
                current_site = get_current_site(request)
                email_subject = "Confirm your email @Quiz Generator"
                message2 = render_to_string('email_confirmation.html',
                                            {'name': myuser.first_name,
                                             'domain': current_site.domain,
                                             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                                             'token': generate_token.make_token(myuser), })
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [myuser.email],
                )
                email.fail_silently = True
                email.send()
                return redirect('index')
        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'authentication/signup.html')
    return render(request, 'authentication/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        print(f"Username: {username}")
        print(f"Entered Password: {pass1}")

        try:
            user1 = User.objects.get(username=username)
        except User.DoesNotExist:
            user1 = None
        print("here")
        print(user1)

        if user1 is not None:
            # print(f"Stored Password (hashed): {user1.password}")
            if pass1 == user1.password:
                # Password matches, log the user in
                print("in")
                login(request, user1)
                fname = user1.first_name
                return render(request, "authentication/index.html", {'fname': fname})
            else:
                # Incorrect password
                messages.error(request, "Bad credentials")
                return redirect('index')
        else:
            # User does not exist
            messages.error(request, "Bad credentials")
            return redirect('index')

    return render(request, 'authentication/signin.html')


def signout(request):
    if request.user.is_authenticated:
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, "Successfully logged out")
    else:
        messages.error(request, "You are not logged in")

    return render(request, 'authentication/signout.html')


def activate(request, uidb64, token):
    print("before")
    try:
        print(uidb64)
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        myuser = User.objects.get(pk=uid)

        print(myuser)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("there")
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('index')
    else:
        return render(request, 'activation_failed.html')
