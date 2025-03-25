from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Income, Expense, UserSettings

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'gender', 'picture']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount']

class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                settings = UserSettings.objects.get(user=user)
                categories = settings.custom_categories or ["Food", "Transport", "Bills"]
                self.fields['category'].choices = [(c, c) for c in categories]
            except UserSettings.DoesNotExist:
                self.fields['category'].choices = [
                    ('Food', 'Food'),
                    ('Transport', 'Transport'),
                    ('Bills', 'Bills'),
                    ('Other', 'Other')
                ]

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category']  # Removed 'date' from here
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['preferred_currency', 'dark_mode', 'custom_categories', 
                 'notify_when_low_balance', 'notify_via_email']
        widgets = {
            'custom_categories': forms.TextInput(attrs={
                'placeholder': 'Comma-separated categories'
            }),
        }