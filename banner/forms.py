from django import forms
from .models import Banner



# banner form


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'


