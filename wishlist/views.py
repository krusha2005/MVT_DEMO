from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.contrib import messages
from products.models import Product
from django.core.exceptions import ValidationError

# Create your views here.
@login_required
def add_to_wishlist(request,id):

    product=get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    messages.success(request,'Product Added In Wishlist')

    return redirect('wishlist')


@login_required
def wishlist(request):

    wishlist_items=Wishlist.objects.filter(
        user=request.user
    )

    return render(request,'wishlist/wishlist.html',{'wishlist_items':wishlist_items})

@login_required
def remove_wish(request,id):

    item=get_object_or_404( Wishlist , id=id)

    item.delete()

    messages.success(request,"Product Removed In Wishlist")

    return redirect('wishlist')