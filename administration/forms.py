from django import forms
from modeltranslation.forms import TranslationModelForm

from orders.models import Order, OrderItem
from shop.models import Category, Product, ProductProperty, ProductPropertyValue, UnitOfMeasure



class ProductForm(TranslationModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'unit_of_measure',
            'price',
            'old_price',
            'stock',
            'description',
            'image',
            'thumbnail',
            'thumbnail2',
            'thumbnail3',
            'available',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'unit_of_measure': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'old_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'thumbnail2': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'thumbnail3': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }



# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name', 'category', 'unit_of_measure', 'price', 'old_price',
#             'stock', 'description', 'image', 'thumbnail', 'thumbnail2',
#             'thumbnail3', 'available'
#         ]
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'custom-input'}),
#             'category': forms.Select(attrs={'class': 'custom-input'}),
#             'unit_of_measure': forms.Select(attrs={'class': 'custom-input'}),
#             'price': forms.NumberInput(attrs={'class': 'custom-input'}),
#             'old_price': forms.NumberInput(attrs={'class': 'custom-input'}),
#             'stock': forms.NumberInput(attrs={'class': 'custom-input'}),
#             'description': forms.Textarea(attrs={'class': 'custom-input'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
#             'thumbnail': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
#             'thumbnail2': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
#             'thumbnail3': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
#             'available': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
#         }



class OrderApprovalForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['paid']
        # widgets = {
        #     'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        #     'address': forms.NumberInput(attrs={'readonly': 'readonly'}),
        # }


# Category
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

# Product property
class CreateProductPropertyForm(forms.ModelForm):
    class Meta:
        model = ProductProperty
        fields = ['name']


class EditUProductPropertyForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit']




# Unit of Measure
class CreateUnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit']


class EditUnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit']

