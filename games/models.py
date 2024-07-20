from django.db import models
from main_category_app.models import Main_category

# Create your models here.


class Games(models.Model):
    name = models.CharField(max_length=200, null=False, blank = False)
    main_category = models.ForeignKey(Main_category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_img', null=True, blank=True)
    description = models.CharField(max_length=500, null=False, blank = False)
    status = models.BooleanField(default = False, help_text="0-show,1-hidden")
    

    def __str__(self):
        return self.name