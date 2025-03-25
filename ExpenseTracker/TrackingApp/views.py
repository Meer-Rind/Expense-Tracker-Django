from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import Profile,Income
from .forms import ProfileForm,IncomeForm

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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('profile')  # Changed to use URL name
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm(request)
        
    return render(request, 'TrackingApp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')



@login_required
def Profile_view(request):
    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'TrackingApp/profile.html', {"form": form})


#creating views for the income
@login_required
def add_income(request):
    if request.method =="POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dhasboard')
    else:
        form = IncomeForm()
    return render(request,'TrackingApp/Income.html',{'form':form})        