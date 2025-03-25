from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[
        ('Male', 'Male'),
        ('Female', 'Female')
    ])
    picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    def __str__(self):
        return self.user.username

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Rent', 'Rent'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField(default=timezone.now)  # Changed from auto_now_add to default
    
    def __str__(self):
        return f"{self.user.username}-{self.name}-{self.amount}"
class UserSettings(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('PKR', 'Pakistani Rupee'),
        ('EUR', 'Euro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_currency = models.CharField(
        max_length=5, 
        choices=CURRENCY_CHOICES, 
        default='USD'
    )
    dark_mode = models.BooleanField(default=False)
    custom_categories = models.JSONField(default=list)
    notify_when_low_balance = models.BooleanField(default=True)
    notify_via_email = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.username}"