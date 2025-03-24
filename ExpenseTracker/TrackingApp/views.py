from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

# Create your views here.

def welcome(request):
    return render(request,'TrackingApp/welcome.html')




def Register_view(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request,user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request,'TrackingApp/register.html',{'form':form})    





def login_view(request):
    if request.method =="POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                messages.success(request,"Login sucesscful")
                return redirect('Home')
            else:
                messages.error(request,'Invalid username or password')
    else:
        form = AuthenticationForm()
        
    return render(request,'TrackingApp/login.html',{'form':form})    



def logout_view(request):
    logout(request)
    return redirect('/login')