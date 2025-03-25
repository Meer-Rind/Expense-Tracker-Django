from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm, IncomeForm, ExpenseForm, UserSettingsForm
from django.db import models
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile, Income, Expense, UserSettings

def welcome(request):
    return render(request, 'TrackingApp/welcome.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'TrackingApp/register.html', {'form': form})

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
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm(request)
    return render(request, 'TrackingApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'TrackingApp/profile.html', {"form": form})

@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'TrackingApp/income.html', {'form': form})

@login_required
def add_expense(request):
    user_income = Income.objects.filter(user=request.user).aggregate(
        total_income=models.Sum('amount')
    )['total_income'] or 0
    
    user_expense = Expense.objects.filter(user=request.user).aggregate(
        total_expense=models.Sum('amount')
    )['total_expense'] or 0
    
    remaining_balance = user_income - user_expense
    settings_obj, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.user = request.user

            if remaining_balance < new_expense.amount:
                messages.warning(
                    request, 
                    "⚠️ Warning: Your expense exceeds your remaining balance!"
                )
                if (settings_obj.notify_when_low_balance and 
                    settings_obj.notify_via_email and 
                    request.user.email):
                    try:
                        send_mail(
                            'Low Balance Alert',
                            f'''Hello {request.user.username},
                            
You are trying to add an expense of {new_expense.amount}, 
but your remaining balance is only {remaining_balance}. 
Please review your expenses.
                            
- Your Expense Tracker''',
                            settings.DEFAULT_FROM_EMAIL,
                            [request.user.email],
                            fail_silently=False,
                        )
                        messages.info(request, "Email notification sent about low balance")
                    except Exception as e:
                        messages.error(request, f"Failed to send email notification: {str(e)}")

            new_expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'TrackingApp/add_expense.html', {
        'form': form,
        'remaining_balance': remaining_balance
    })

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expense = sum(exp.amount for exp in expenses) if expenses else 0
    total_income = sum(inc.amount for inc in Income.objects.filter(user=request.user)) if Income.objects.filter(user=request.user) else 0
    remaining_balance = total_income - total_expense
    
    return render(request, 'TrackingApp/expense_list.html', {
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_balance': remaining_balance,
    })

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')
    return render(request, 'TrackingApp/delete.html', {'expense': expense})

@login_required
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-date')
    income = Income.objects.filter(user=user).order_by('-date')
    
    total_income = sum(i.amount for i in income) if income else 0
    total_expense = sum(e.amount for e in expenses) if expenses else 0
    remaining_income = total_income - total_expense
    
    monthly_expenses = {}
    for expense in expenses:
        month = expense.date.strftime('%Y-%m')
        monthly_expenses[month] = monthly_expenses.get(month, 0) + expense.amount
        
    category_expenses = {}
    for expense in expenses:
        category_expenses[expense.category] = category_expenses.get(expense.category, 0) + expense.amount
    
    return render(request, 'TrackingApp/dashboard.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_income': remaining_income,
        'monthly_expenses': monthly_expenses,
        'category_expenses': category_expenses,
    })

@login_required
def settings_view(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserSettingsForm(instance=settings)
    return render(request, 'TrackingApp/settings.html', {'form': form})

@login_required
def get_expense_data(request):
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    labels = [expense.date.strftime("%Y-%m-%d") for expense in expenses]
    data = [expense.amount for expense in expenses]
    return JsonResponse({'labels': labels, 'data': data})

@login_required
def get_income_expense_data(request):
    total_income = Income.objects.filter(user=request.user).aggregate(
        models.Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(
        models.Sum('amount'))['amount__sum'] or 0
    return JsonResponse({'income': total_income, 'expense': total_expense})