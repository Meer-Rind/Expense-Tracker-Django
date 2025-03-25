from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#creating a model for the Profile which wilkl contain the follwing fieldsfirstone will be the field for the nane,second for the phone third for the gvender and then for the picture
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)#creating a user field that will be associated with the user model menas every user has a profile
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[('Male','Male'),('Female','Female')])
    picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    
    def __str__(self):
        return self.user.username\
            
#creating a model for the income
#it will also have a relation wiht the model user
class Income(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.amount}"#will show the name of the user and also it's amount whihc he had in the account