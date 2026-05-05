from django.db import models
from django.core.exceptions import ValidationError
from products.utils.image_compress import compress_image
import os

def validate_image(image):
    if image.size > 1 * 1024 * 1024:
        raise ValidationError("Image size should be less than 1MB")

    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError("Only JPG and PNG allowed")

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='categories/',
        validators=[validate_image],
        null=True,
        blank=True
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
        super().save(*args, **kwargs)

        if self.image:
            self.image.save(
                self.image.name,
                compress_image(self.image),
                save=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            self.image.save(
                self.image.name,
                compress_image(self.image),
                save=False
            )

        super().save(*args, **kwargs)