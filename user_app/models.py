from django.db import models
from auth_app.models import Customuser

# Create your models here.



# Address user model


class Address(models.Model):
    user = models.ForeignKey(Customuser, on_delete = models.CASCADE, null = True, blank = True)
    full_name = models.CharField(max_length = 200)
    house_no = models.CharField(max_length = 200)
    post_code = models.CharField(max_length = 30)
    state = models.CharField(max_length =50)
    street = models.CharField(max_length=150)
    phone_no = models.CharField(max_length = 15, blank = True)
    city = models.CharField(max_length = 100)
    is_delete = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.full_name