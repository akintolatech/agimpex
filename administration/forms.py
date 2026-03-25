from django import forms
from shop.models import Category, Product, ProductProperty, ProductPropertyValue


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # We include slug here if you want the user to type it manually
        fields = ['name', 'icon']


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon']

        # widgets = {
        #     # 'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        #     'reference_code': forms.TextInput(attrs={'readonly': 'readonly'}),
        #     'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        #     'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        # }
