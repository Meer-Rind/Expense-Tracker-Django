from django.contrib import admin
from .models import Profile,Income,Expense,UserSettings
# Register your models here.

admin.site.register(Profile)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(UserSettings)
