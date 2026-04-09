from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category, ProductProperty

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class ProductPropertyTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(ProductProperty, ProductPropertyTranslationOptions)