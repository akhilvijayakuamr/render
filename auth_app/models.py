from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


# User Model 

class Customuser(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
    user_bio = models.CharField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    refferal = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.username
    
#Banner add
    


    
   



    