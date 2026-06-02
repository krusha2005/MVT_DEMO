import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from products.models import Product
from django.contrib import messages
from django.db.models import Q, Count

@login_required
def checkout(request):
    cart_items=CartItem.objects.filter(
        cart__user=request.user
    )

    total=0
    out_of_stock_products=[]
    for item in cart_items:
        total+= item.product.price * item.quantity

        product = item.product
        if product.stock < item.quantity:
            out_of_stock_products.append(item)

    # if out_of_stock_products:
    #     for product in out_of_stock_products:
    #         product.delete()
    #     messages.error(request,f"{' ,'.join([item.product.name for item in out_of_stock_products])} are out of stock!")
    #     return redirect('cart')

    if out_of_stock_products:
        messages.error(request,'please remove out-of-stock products!')
        return redirect('cart')

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

    cart_items=CartItem.objects.select_related(
        'product'
    ).filter(
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

    if not phone.isdigit() or len(phone)!=10:
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

    if buy_product_id:

        product=get_object_or_404(
            Product,
            id=buy_product_id
        )
        buy_quantity = int(request.POST.get('quantity',1))

        buy_total = product.price * buy_quantity

        order= Order.objects.create(
            buyer=request.user,
            order_id=f"ORD{random.randint(1000,9999)}",
            total_amount=buy_total,
            message="your order has been placed successfully!",

            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            seller=product.seller,
            quantity=buy_quantity,
            price=product.price,
            total_price=buy_total
        )

        product.stock -= buy_quantity
        product.save()

        CartItem.objects.filter(cart__user=request.user,product=product).delete()

    else:

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


@login_required
def seller_orders(request):

    search=request.GET.get('search')

    '''show only login seller orders list  nd LIFO'''
    orders=OrderItem.objects.select_related(
        'order',
        'product'
    ).filter(
        seller=request.user
    ).order_by('-id')

    # orders=OrderItem.objects.all().order_by('-id')

    '''for search by orderID , product ,buyer name'''
    if search:
        orders = orders.filter(
            Q(order__order_id__icontains = search) |
            Q(product__name__icontains = search) |
            Q(order__buyer__username__icontains = search)
        )

    if not orders.exists():
        messages.warning(request,'No matching orders found! showing all orders')

        orders=OrderItem.objects.filter(
            seller=request.user
        ).order_by('-id')

    '''for filter by status'''
    status_type=request.GET.get('status_type')

    if status_type:
        orders=orders.filter(
            status = status_type
        )

    return render(request,'orders/seller_orders.html',{
        'orders':orders,
    })


@login_required
def seller_order_detail(request,id):

    '''for 1 order only for detail'''
    order = get_object_or_404(
        OrderItem,
        id=id,
        seller=request.user
    )

    return render(request,'orders/seller_order_detail.html',{
        'order':order
    })


@login_required
def update_order_status(request,id):

    order = get_object_or_404(
        OrderItem,
        id=id,
        seller=request.user
    )

    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()

    return redirect('seller_order_detail',id=order.id)



@login_required
def buyer_dashboard(request):

    total_orders = Order.objects.filter(
        buyer=request.user
    ).count()

    order_item_stats = OrderItem.objects.filter(
        order__buyer = request.user
    ).aggregate(
        pending_orders = Count('id', filter= Q(status = 'Pending')),
        delivered_orders = Count('id', filter= Q( status = 'Delivered'))
    )

    cart_items = CartItem.objects.filter(
        cart__user=request.user
    ).count()

    current_orders = OrderItem.objects.select_related(
        'product',
        'order'
    ).filter(
        order__buyer=request.user
    ).order_by('-id')

    search = request.GET.get('search')

    if search:

        current_orders = current_orders.filter(
            Q( order__order_id__icontains = search) |
            Q( product__name__icontains = search) |
            Q( status__icontains = search)
        )

    return render(
        request,
        'orders/buyer_dashboard.html',
        {
            'total_orders': total_orders,
            'pending_orders': order_item_stats['pending_orders'],
            'delivered_orders': order_item_stats['delivered_orders'],
            'cart_items': cart_items,
            'current_orders': current_orders
        }
    )

@login_required
def buyer_order_detail(request,id):

    order = get_object_or_404(
        OrderItem.objects.select_related(
            'order',
            'product'
        ),
        id=id,
        order__buyer=request.user
    )

    return render(request,'orders/buyer_order_detail.html',
        {
            'order': order
        }
    )