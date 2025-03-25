from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Profile,Income

#create forms here
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # first_name = forms.CharField(required=True,max_length=100)
    # last_name = forms.CharField(required=True,max_length=100)
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
        
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','phone','gender','picture']        
        
#creating form for the Income
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount']        