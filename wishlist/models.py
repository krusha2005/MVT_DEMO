from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product

# Create your models here.
class Wishlist(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE )

    created_at = models.DateTimeField( auto_now_add=True )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"