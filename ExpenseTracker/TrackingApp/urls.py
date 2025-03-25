from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name="profile"),
    path('income/', views.add_income, name="income"),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_list/', views.expense_list, name='expense_list'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('api/expense-data/', views.get_expense_data, name='get_expense_data'),
    path('api/income-expense-data/', views.get_income_expense_data, name='get_income_expense_data'),
]