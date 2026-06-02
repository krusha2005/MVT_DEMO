from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import SellerProfile, User
from .forms import LoginForm, BuyerRegisterForm, SellerRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Category
from orders.models import OrderItem, Order
from cart.models import CartItem
from django.db.models import Q, Count
from django.db.models import Prefetch


# for register choice page
def register_choice(request):
    return render(request, 'accounts/register_choice.html')

# for buyer side register
def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # use only if form inlcude thosew field in meta

            user.role = 'buyer'
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()

            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')   # we will create login next

    else:
        form = BuyerRegisterForm()

    return render(request, 'accounts/buyer_register.html', {'form': form})


# # for login for buyer nd seller both
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)

#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)

#             # 🔥 role-based redirect
#             if user.is_superuser:
#                 return redirect('admin_dashboard')
#             elif user.role == 'seller':
#                 return redirect('home')
#             else:
#                 return redirect('home')


#     else:
#         form = LoginForm()

#     return render(request, 'accounts/login.html', {'form': form})

# for login for buyer nd seller both
def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        username=request.POST.get('username')
        password=request.POST.get('password')

        # username not exist

        if not User.objects.filter( username=username ).exists():
            form.add_error('username','Username does not exist!')

        else:
            user = authenticate(request,
                                username=username,
                                password=password)
            
            if user is None:
                form.add_error('password','Invalid Password!')
            else:
                login(request,user)

                return redirect('home')

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # role-based redirect
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'seller':
                return redirect('home')
            else:
                return redirect('home')


    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# for seller side register

def seller_register(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'seller'
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 2. create seller profile (ONLY store_name here)
            seller = SellerProfile.objects.create(
                user=user,
                store_name=form.cleaned_data['store_name']
            )

            # 3. optional categories
            seller.categories.set(form.cleaned_data['categories'])

            return redirect('login')

    else:
        form = SellerRegisterForm()

    return render(request, 'accounts/seller_register.html', {'form': form})


# @login_required
# def seller_dashboard(request):
#     user = request.user

#     # seller profile
#     seller_profile = user.seller_profile

#     # categories seller selected
#     categories = seller_profile.categories.all()

#     # seller products
#     products = Product.objects.filter(seller=user)

#     context = {
#         'categories': categories,
#         'products': products
#     }

#     return render(request, 'accounts/seller_dashboard.html', context)


@login_required
def seller_dashboard(request):
    user = request.user

    try:
        seller = user.seller_profile
    except:
        # recreate profile if missing
        seller = SellerProfile.objects.create(user=user)

    categories = seller.categories.all()


    product = user.products.select_related(
        'product_type'
    ).prefetch_related(
        'images'
    ).filter(
        is_deleted = False
    ).order_by('-id')

    total_products = Product.objects.filter(
        seller=request.user
    ).count()

    order_item_stats = OrderItem.objects.filter(
        seller = request.user
    ).aggregate(
        pending_orders = Count('id', filter= Q(status = 'Pending')),
        delivered_orders = Count('id', filter= Q( status = 'Delivered')),
        total_orders = Count('id')
    )

    recent_orders = OrderItem.objects.filter(
        seller = request.user
    ).order_by('-id')[:5]

    return render(request, 'accounts/seller_dashboard.html', {
        'categories': categories,
        'products' : product,

        'total_products' : total_products,
        'total_orders' : order_item_stats['total_orders'],
        'pending_orders': order_item_stats['pending_orders'],
        'delivered_orders': order_item_stats['delivered_orders'],
    })

@login_required
def out_of_stock(request):

    products = Product.objects.filter(
        seller = request.user,
        stock = 0
    )

    return render(request, 'accounts/out_of_stock.html',{
        'products':products
    })


@login_required
def deleted_products(request):

    products = Product.objects.prefetch_related(
        'images'
    ).filter(
        seller = request.user,
        is_deleted = True
    ).order_by('-id')


    return render(request,'accounts/deleted_products.html',{
                      'products' : products ,
                  })


@login_required
def deleted_product_buyers(request ,id):

    product = get_object_or_404(
        Product,
        id = id,
        seller = request.user,
        is_deleted = True
    )

    cart_items = CartItem.objects.select_related(
        'cart',
        'cart__user'
    ).filter(
        product = product
    )

    return render(request,'accounts/deleted_product_buyers.html',{
        'product' : product,
        'cart_items' : cart_items
    })

def admin_required(user):
    return user.is_superuser


@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):

    total_seller_buyer = User.objects.aggregate(
        total_seller = Count('id', filter= Q(role = 'seller')),
        total_buyer= Count('id', filter= Q( role = 'buyer'))
    )

    total_products = Product.objects.filter(
        is_deleted= False
    ).count()

    total_orders =Order.objects.count()

    sellers = SellerProfile.objects.select_related(
        'user',
    ).prefetch_related(
        'categories'
    ).order_by('-id')

    buyers = User.objects.prefetch_related(
        'orders'
    ).filter(
        role = 'buyer'
    ).order_by('-id')

    categories = Category.objects.prefetch_related(
        'subcategories__product_types'
    )

    return render(request,'accounts/admin_dashboard.html',{
        'total_seller' : total_seller_buyer['total_seller'] , 
        'total_buyer' : total_seller_buyer['total_buyer'],
        'total_products' : total_products,
        'total_orders' : total_orders,
        'sellers' : sellers,
        'buyers' : buyers,
        'categories' : categories
    })


@login_required
@user_passes_test(admin_required)
def admin_seller_detail(request,id):

    seller = get_object_or_404(
        SellerProfile.objects.select_related(
            'user'
        ),
        id =id
    )

    products = Product.objects.filter(
        seller = seller.user,
        is_deleted = False
    ).order_by('-id')

    return render(request,'accounts/admin_seller_detail.html',{
        'seller' : seller,
        'products' : products
    })

@login_required
@user_passes_test(admin_required)
def admin_buyer_detail(request,id):

    buyer = get_object_or_404(
        User.objects.prefetch_related(
            'orders',
            'wishlist_set',
            
        ),
        role = 'buyer',
        id=id
    )

    order = OrderItem.objects.select_related(
        'order',
        'product'
    ).filter(
        order__buyer=buyer,   
        # left side must be actual model field nd right side actual python  object/value 

    ).order_by('-id')

    return render(request,'accounts/admin_buyer_detail.html',{
        'buyer': buyer,
        'orders':order

    })

@login_required
@user_passes_test(admin_required)
def delete_seller(request,id):

    seller = get_object_or_404(
        SellerProfile,
        id=id
    )

    seller.user.delete()

    messages.success(request ,'seller deleted successfully!')

    return redirect('admin_dashboard')


@login_required
@user_passes_test(admin_required)

def delete_buyer(request,id):

    buyer = get_object_or_404(
        User,
        role = 'buyer',
        id=id
    )

    buyer.delete()

    messages.success(request,'buyer deleted successfully!')

    return redirect('admin_dashboard')