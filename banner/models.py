from django.db import models
from products.models import Product

# Create your models here.


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='banner')
    offer = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return self.id

