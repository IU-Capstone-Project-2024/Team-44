from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request): 
    return render(request, 'authentication/index.html')

def signup (request): 
    if request.method == "POST": 
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        telegram_id = request.POST['telegram-id']
        myuser = User.objects.create(username = username, email=email, password = pass1, 
                                     first_name = fname, last_name = lname, telegram_id = telegram_id )
        
        myuser.save()
        messages.success(request, 'Your account have been successfully created.')
        return redirect('signin')
    return render (request, 'authentication/signup.html')


def signin (request): 
    if request.method == 'POST': 
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password = pass1)
        if user is not None: 
            login(request, user)
            fname = user.firstname 
            return render(request, "authentication/index.html", {'fname': fname})
        else: 
            messages.error(request, "Bad credentials")
            return redirect('index')
    return render (request, 'authentication/signin.html')


def signout (request): 
    return render (request, 'authentication/signout.html')

 