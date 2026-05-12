from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    total_amount= models.DecimalField(max_digits=10,decimal_places=2)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True)

    name = models.CharField(max_length=20,null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    state = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.order_id
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey( Product,on_delete=models.CASCADE)
    seller = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    total_price = models.DecimalField( max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.name