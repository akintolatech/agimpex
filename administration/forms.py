from django import forms
from modeltranslation.forms import TranslationModelForm

from orders.models import Order, OrderItem
from shop.models import Category, Product, ProductProperty, UnitOfMeasure


from django import forms

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'administration/product/custom_clearable_file_input.html'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'name_hy',
            'name_ru',
            'category',
            'unit_of_measure',
            'price',
            'old_price',
            'stock',
            'description',
            'description_hy',
            'description_ru',
            'image',
            'thumbnail',
            'thumbnail2',
            'thumbnail3',
            'available',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter English name'
            }),
            'name_hy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Armenian name'
            }),
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Russian name'
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
                'placeholder': 'Enter English description'
            }),
            'description_hy': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter Armenian description'
            }),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter Russian description'
            }),

            'image': CustomClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': CustomClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail2': CustomClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail3': CustomClearableFileInput(attrs={'class': 'form-control'}),

            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


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
        fields = ['name', 'name_hy', 'name_ru']


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',  'name_hy', 'name_ru']

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
        fields = ['name', 'name_hy', 'name_ru']


class EditUProductPropertyForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit']

# Unit of Measure
class CreateUnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit', 'unit_hy', 'unit_ru']


class EditUnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['unit']

