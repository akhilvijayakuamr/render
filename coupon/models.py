from django.db import models

# Create your models here.

#Coupon model 

class Coupon(models.Model):
    coupon_code     =  models.CharField(max_length=100)
    expired         =  models.BooleanField(default=False)
    discount_price  =  models.PositiveIntegerField(default=100)
    minimum_amount  =  models.PositiveIntegerField(default=500)
    expiry_date     =  models.DateField(null=True,blank=True)
    
    def _str_(self):
        return self.coupon_code