from django import forms
from .models import Main_category



class CategoreyForm(forms.ModelForm):
    class Meta:
        model = Main_category
        fields = '__all__'