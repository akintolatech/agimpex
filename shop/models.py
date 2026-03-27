from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="cat_icons", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )

    thumbnail = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )

    thumbnail2 = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )

    thumbnail3 = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )

    description = models.TextField(blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    @property
    def discount_amount(self):
        if self.old_price:
            return self.old_price - self.price
        return 0

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > 0:
            return round(((self.old_price - self.price) / self.old_price) * 100, 2)
        return 0

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

        if self.old_price is not None:
            if self.old_price < 0:
                raise ValidationError("Old price cannot be negative.")
            if self.old_price < self.price:
                raise ValidationError("Old price should be greater than or equal to price.")


class ProductProperty(models.Model):
    """
    Example: Thickness, Row Height, Color, Size
    """
    product = models.ForeignKey(
        Product,
        related_name='attributes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name')
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductPropertyValue(models.Model):
    """
    Example values for an attribute:
    Thickness -> 5mm, 10mm
    Row Height -> 100cm, 120cm
    """
    attribute = models.ForeignKey(
        ProductProperty,
        related_name='values',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('attribute', 'value')
        ordering = ['id']

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class UnitOfMeasure(models.Model):
    unit = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.unit}"