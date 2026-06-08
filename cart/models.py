from django.db import models
from django.conf import settings

from products.models import Product


class Cart(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.user.username 

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.name 