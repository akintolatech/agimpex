from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="cat_icons", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

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
        return reverse('shop:product_list_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class UnitOfMeasure(models.Model):
    unit = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['unit']
        verbose_name = 'Unit of Measure'
        verbose_name_plural = 'Units of Measure'

    def __str__(self):
        return self.unit


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        related_name='products',
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

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

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
        if self.old_price is not None and self.old_price > self.price:
            return self.old_price - self.price
        return 0

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > 0 and self.old_price > self.price:
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class ProductProperty(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='properties',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name')
        ordering = ['id']
        verbose_name = 'Product Property'
        verbose_name_plural = 'Product Properties'

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductPropertyValue(models.Model):
    product_property = models.ForeignKey(
        ProductProperty,
        related_name='property_values',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        unique_together = ('product_property', 'value')
        ordering = ['id']
        verbose_name = 'Product Property Value'
        verbose_name_plural = 'Product Property Values'

    def __str__(self):
        return f"{self.product_property.name}: {self.value}"