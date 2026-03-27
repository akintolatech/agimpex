from django import forms

from orders.models import Order, OrderItem
from shop.models import Category, Product, ProductProperty, ProductPropertyValue


class OrderApprovalForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['paid']
        # widgets = {
        #     'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        #     'address': forms.NumberInput(attrs={'readonly': 'readonly'}),
        # }



class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
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
