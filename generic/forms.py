from django.forms import ModelForm
from substitution.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = []
