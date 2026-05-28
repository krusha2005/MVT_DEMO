from django.db import models
from django.core.exceptions import ValidationError
from products.utils.image_compress import compress_image
import os
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_image(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Image size should be less than 2MB")

    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError("Only JPG and PNG allowed")

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='categories/',
        validators=[validate_image],
        # null=True,
        # blank=True
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategories/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    '''for now we have require field value can not we null so become db error for that we use null=true after we add then we can null=False'''
    category = models.ForeignKey('Category', on_delete=models.CASCADE,null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, null=True)
    '''# after change null=false'''

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(50)], help_text="Stock must be at least 1.",default=1 )

    is_deleted = models.BooleanField( default=False )

    created_at = models.DateTimeField(default=timezone.now)
    '''# after change auto_now_Add=true'''

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = compress_image(self.image)

    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='product_types'
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_types/', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/', validators=[validate_image])

    def save(self, *args, **kwargs):
        validate_image(self.image)
        if self.image:
            self.image = compress_image(self.image)

        super().save(*args, **kwargs)
