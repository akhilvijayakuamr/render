from  django import forms
from .models import Product, Image

#product  Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

#image form
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

# review Form
        
# class ProductReviewForm(forms.ModelForm):
#     class Meta:
#         model = ProductReview
#         fields = ('review_text', 'review_rating')



