from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages 
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
        myuser = User.objects.create(username = username, email=email, password = pass1)
        myuser.first_name = fname 
        myuser.last_name =  lname 
        myuser.save()
        messages.success(request, 'Your account have been successfully created.')
        return redirect('signin')
    return render (request, 'authentication/signup.html')


def signin (request): 
    return render (request, 'authentication/signin.html')


def signout (request): 
    return render (request, 'authentication/signout.html')

 