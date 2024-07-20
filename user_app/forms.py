from django import forms
from auth_app.models import Customuser


class Userupdateform(forms.ModelForm):
    class Meta:
        model = Customuser
        fields = '__all__'



