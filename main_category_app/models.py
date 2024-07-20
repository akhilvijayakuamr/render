from django.db import models

# Create your models here.


class Main_category(models.Model):
    name = models.CharField(max_length=200, null=False, blank = False)
    image = models.ImageField(upload_to='main_img', null=True, blank=True)
    description = models.CharField(max_length=500, null=False, blank = False)
    category_offer_description = models.CharField(max_length=100, null=True, blank=True)
    category_offer = models.PositiveBigIntegerField(default=0)
    status = models.BooleanField(default = False, help_text="0-show,1-hidden")

    def __str__(self):
        return self.name
