from django.db import models
from auth_app.models import Customuser
from checkout.models import Order

# Create your models here.


class Wallet(models.Model):
    user  =models.ForeignKey(Customuser, on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_credit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,blank=True)

    def str(self):
        return f"{self.amount} {self.is_credit}"

    def iter(self):
        yield self.pk