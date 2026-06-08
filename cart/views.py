from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from wishlist.models import Wishlist
from django.urls import reverse


@login_required
def add_to_cart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    '''for stock if it out of stock then return in product detail nd buyer can't buy'''
    if product.stock <= 0:
        messages.error(request,'product is out of stock')
        return redirect('product_detail',id=product.id)

    '''for in cart if product is already in cart then it increase product'''
    if not created:

        if (cart_item.quantity < 5 and cart_item.quantity < product.stock):
            cart_item.quantity += 1
            cart_item.save()

    '''for in wishlist id that product add in cart then remove from wishlist'''
    Wishlist.objects.filter(user=request.user,product=product).delete()

    messages.success(request,"Product added to cart")
    return redirect('cart')


@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # cart_items = CartItem.objects.filter(cart = cart).select_related(
    #     'product',
    #     'product__seller',
    # ).prefetch_related('product__images')

    cart_items = cart.items.all().select_related(
        'product',
        'product__seller',
    ).prefetch_related('product__images')

    total = 0
    for item in cart_items:
        total += item.total_price()

    return render(request,'cart/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )

@login_required
def increase_quantity(request,id):

    item=get_object_or_404( CartItem ,id=id)

    if(item.quantity < 5 and item.quantity < item.product.stock):
        item.quantity += 1
        item.save()

        return redirect('cart')

    return redirect(f"{reverse('cart')}?error_item={item.id}")

@login_required
def decrease_quantity(request,id):

    item=get_object_or_404( CartItem, id=id)
    if(item.quantity > 1):
        item.quantity -= 1
        item.save()
    else:
        item.delete()
        return redirect('cart')
    
    return redirect(f"{reverse('cart')}?error_item={item.id}")

@login_required
def remove_cart_item(request,id):

    item=get_object_or_404(CartItem, id=id)
    item.delete()

    return redirect('cart')

         
