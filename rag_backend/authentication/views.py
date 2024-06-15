from time import sleep
from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
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
                myuser = User.objects.create(username = username, email=email, 
                                             password = pass1, first_name=fname, last_name = lname, telegram_id = telegram_id)
                
                myuser.save()
                messages.success(request, 'Your account has been successfully created.')
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
        print (user1) 
        
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


def signout (request): 
    logout(request) 
    messages.success(request, "Successfully logged out")
    return render (request, 'authentication/signout.html')

   