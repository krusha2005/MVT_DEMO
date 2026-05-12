import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from products.models import Product
from django.contrib import messages

@login_required
def checkout(request):
    cart_items=CartItem.objects.filter(
        cart__user=request.user
    )

    total=0
    for item in cart_items:
        total+= item.product.price * item.quantity

    return render(request,'orders/checkout.html',{
        'cart_items':cart_items,
        'total':total
    })

@login_required
def buy_now(request,id):

    product=get_object_or_404(
        Product,
        id=id
    )

    total=product.price

    '''for stock if it out of stock then return in product detail nd buyer can't buy'''
    if product.stock <= 0:
        messages.error(request,'product is out of stock')
        return redirect('product_detail',id=product.id)

    return render(request,'orders/checkout.html',
                  {
                      'buy_product':product,
                      'total':total
                  })


@login_required
def place_order(request):

    cart_items=CartItem.objects.filter(
        cart__user=request.user
    )

    total=0
    for item in cart_items:
        total+= item.product.price * item.quantity

    name=request.POST.get('name')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    buy_product_id=request.POST.get('buy_product_id')

    if len(phone)!=10:
        return render(request,'orders/checkout.html',{
            'phone_error':'phone number must be 10 digits!',
            'cart_items':cart_items,
            'total':total,
            'name': name,
            'phone': phone,
            'address': address,
            'city': city,
            'state': state,
        })

    order= Order.objects.create(
        buyer=request.user,
        order_id=f"ORD{random.randint(1000,9999)}",
        total_amount=total,
        message="your order has been placed successfully!",

        name=name,
        phone=phone,
        address=address,
        city=city,
        state=state

    )

    if buy_product_id:

        product=get_object_or_404(
            Product,
            id=buy_product_id
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            seller=product.seller,
            quantity=1,
            price=product.price,
            total_price=product.price
        )

        product.stock -= 1
        product.save()

        CartItem.objects.filter(cart__user=request.user,product=product).delete()
        
    else:

        for item in cart_items:
            product = item.product

            if product.stock >= item.quantity:
                OrderItem.objects.create(

                    order=order,
                    product=product,
                    seller=product.seller,
                    quantity=item.quantity,
                    price=product.price,
                    total_price=product.price * item.quantity
                )

                # UPDATE STOCK
                product.stock -= item.quantity
                product.save()

        cart_items.delete()
 
    return render(request,'orders/checkout.html',
                  {
                    'success': True,
                    'order': order,
                    'cart_items': [],
                    'total': 0
                })