from django.db import models
from games.models import Games
from auth_app.models import Customuser
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    catagory = models.ForeignKey(Games,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    vender = models.CharField(max_length=150,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    orginal_price = models.FloatField(null=False,blank=False)
    description = models.CharField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-hidden")
    img = models.ImageField(upload_to='prod')
    product_offer = models.PositiveBigIntegerField(default=0)
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        if self.product_offer != 0:
            return self.orginal_price-(self.orginal_price*self.product_offer//100)
        else:
            return self.orginal_price
        
    @property
    def selling_price(self):
        Totel=0
        offer = None
        if self.catagory.main_category.category_offer:
            offer = self.catagory.main_category.category_offer
            Totel = self.orginal_price-(offer*self.orginal_price //100)
            if self.product_offer:
                if offer < self.product_offer:
                    offer = self.product_offer
                    Totel = self.orginal_price-(offer*self.orginal_price //100)
                else:
                    Totel = self.orginal_price-(offer*self.orginal_price //100)
        elif self.product_offer:
            offer = self.product_offer
            Totel=self.orginal_price-(offer*self.orginal_price //100)
        else:
            Totel=self.orginal_price
        return Totel 
    

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')







# review rating view


class Review(models.Model):
    user = models.ForeignKey(Customuser, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    review_text = models.TextField(max_length=250)
    review_rating = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days_ago(self):
        now = timezone.now()
        time_difference = now - self.created_at
        return time_difference.days

    def __str__(self) -> str:
        return self.id