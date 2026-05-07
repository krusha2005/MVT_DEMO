# from django.shortcuts import render, redirect

# def home(request):
#     return render(request, 'home.html')


# def seller_dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     if request.user.role != 'seller':
#         return redirect('home')

#     return render(request, 'seller/dashboard.html')

from django.shortcuts import render
from products.models import Product, Category

# def home(request):
#     user = request.user

#     # seller profile
#     seller_profile = user.seller_profile

#     # categories seller selected
#     categories = seller_profile.categories.all()

#     # seller products
#     products = Product.objects.filter(seller=user)
#     products = Product.objects.select_related('category', 'subcategory').all()

#     return render(request, 'home.html', {
#         'categories': categories,
#         'products': products
#     })

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')

    seller_categories = None

    # ✅ FIX: check login
    if request.user.is_authenticated:
        user = request.user

        # ✅ check if seller
        if hasattr(user, 'seller_profile'):
            seller_categories = user.seller_profile.categories.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'seller_categories': seller_categories
    })

