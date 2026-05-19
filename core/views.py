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
from products.models import Product, Category, SubCategory, ProductType
from accounts.models import SellerProfile
from django.db.models import Q
from django.contrib import messages
from django.db.models import Count

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




# def home(request):
#     categories = Category.objects.all()
#     products = Product.objects.all().order_by('-id')

#     seller_categories = None

#     # SEARCH
#     search = request.GET.get('search')

#     if search:
#         products = products.filter(
#             Q(name__icontains=search) |
#             Q(seller__seller_profile__store_name__icontains=search ) |
#             Q(category__name__icontains=search) |
#             Q(subcategory__name__icontains=search) |
#             Q(product_type__name__icontains=search)  )

#     # CATEGORY FILTER

#     categories = Category.objects.all()

#     '''ALWAYS fetch all subcategories so the dropdown is populated
#        We will use JavaScript to hide the ones we don't need'''

#     subcategories = SubCategory.objects.all()

#     # products = Product.objects.all()

#     '''Get filter values from URL'''
#     cat_id = request.GET.get('category')
#     sub_id = request.GET.get('subcategory')
#     # search = request.GET.get('search')

#     '''Apply filters ONLY if the values exist in the URL (after Search is clicked)'''
#     if search:
#         products = products.filter(name__icontains=search)
#     if cat_id:
#         products = products.filter(category_id=cat_id)
#     if sub_id:
#         products = products.filter(subcategory_id=sub_id)

#     context = {
#         'categories': categories,
#         'subcategories': subcategories,
#         'products': products,
#     }

#     # PRODUCT TYPE FILTER
#     product_type = request.GET.get('product_type')

#     if product_type:
#         products = products.filter(
#             product_type_id=product_type
#         )

#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     if min_price:
#         products = products.filter(
#             price__gte=min_price
#         )

#     if max_price:
#         products = products.filter(
#             price__lte=max_price
#         )

#     categories = Category.objects.all()
#     product_types = ProductType.objects.all()

#     # ✅ FIX: check login
#     if request.user.is_authenticated:
#         user = request.user

#         # ✅ check if seller
#         if hasattr(user, 'seller_profile'):
#             seller_categories = user.seller_profile.categories.all()

#     return render(request, 'home.html', {
#         'categories': categories,
#         'products': products,
#         'seller_categories': seller_categories,
#         'subcategories': subcategories,
#         'product_types': product_types,
#         'context':context
#     })


def home(request):

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    product_types = ProductType.objects.all()

    products = Product.objects.filter(
        is_deleted = False
    ).order_by('-id')

    seller_categories = None

    # SEARCH
    search = request.GET.get('search')

    if search:
        products = products.filter(

            Q(name__icontains=search) |

            Q(seller__seller_profile__store_name__icontains=search) |

            Q(category__name__icontains=search) |

            Q(subcategory__name__icontains=search) |

            Q(product_type__name__icontains=search)

        )

    # FILTERS
    cat_id = request.GET.get('category')
    sub_id = request.GET.get('subcategory')
    product_type_id = request.GET.get('product_type')

    if cat_id:
        products = products.filter(
            category_id=cat_id
        )

    if sub_id:
        products = products.filter(
            subcategory_id=sub_id
        )

    if product_type_id:
        products = products.filter(
            product_type_id=product_type_id
        )

    # PRICE FILTER
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    if not products.exists():

        messages.warning(
            request,
            "No matching products found. Showing all products."
        )

        products = Product.objects.filter(
            is_deleted = False
        ).order_by('-id')


    # SELLER CATEGORY
    if request.user.is_authenticated:

        user = request.user

        if hasattr(user, 'seller_profile'):

            seller_categories = (
                user.seller_profile.categories.all()
            )

    best_seller = Product.objects.filter(
        orderitem__status = 'Delivered'
    ).annotate(total_sold = Count('orderitem')).order_by('-total_sold')[:4]

    if not ( search or cat_id or sub_id or product_type_id or min_price or max_price ):
        products = products.exclude(
            id__in=best_seller.values_list('id', flat=True)
        )

    return render(request, 'home.html', {

        'categories': categories,
        'subcategories': subcategories,
        'product_types': product_types,
        'products': products,
        'seller_categories': seller_categories,
        'best_sellers' : best_seller 
    })
