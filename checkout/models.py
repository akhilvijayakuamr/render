
from django.db import models
from auth_app.models import Customuser
from user_app.models import Address
from products.models import Product
from datetime import date
# Create your models here.
class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("processing", "processing"),
        ("shipped", "shipped"),
        ("delivered", "delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("refunded", "refunded"),
        ("on_hold", "on_hold"),
    )

    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order_address')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name='order_product'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default="pending")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    date = models.DateField(default=date.today)
    # coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.product}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem_product')
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return str(self.id)