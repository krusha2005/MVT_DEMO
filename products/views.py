from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ProductImageForm
from .models import Category, SubCategory, ProductType, ProductImage
from django.contrib import messages
from products.models import Product
from django.core.exceptions import ValidationError


def add_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'category/add.html', {'form': form})

def select_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()

    return render(request, 'products/select_subcategory.html', {
        'category': category,
        'subcategories': subcategories
    })


@login_required
def select_product_type(request, category_id, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    types = subcategory.product_types.all()


    '''after select product type add product in form'''
    selected_type = None 

    if request.method == 'POST':
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')
        type_id = request.POST.get('type_id')

        # ✅ STEP 1: check type_id FIRST
        if not type_id:
            form = ProductForm(request.POST)
            form.add_error(None, "Please select a product type first")

            return render(request, 'products/select_product_type.html', {
                'subcategory': subcategory,
                'types': types,
                'form': form
            })

        # ✅ STEP 2: NOW safe to fetch
        product_type = get_object_or_404(ProductType, id=type_id)

        # ✅ STEP 3: continue normal flow
        form = ProductForm(request.POST)

        if len(images) > 5:
            form.add_error(None, "You can upload maximum 5 images only")

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.product_type = product_type
            product.subcategory = product_type.subcategory
            product.category = product_type.subcategory.category
            product.save()

            '''try except for if image is >2mb then it handle'''
            try:
                for img in images:
                    ProductImage.objects.create(
                        product=product,
                        image=img
                    )

            except ValidationError as e:
                form.add_error(None, e.messages[0])
                product.delete()

                return render(request,'products/select_product_type.html',
                    {
                        'form': form,
                        'types': types,
                        'subcategory': subcategory,
                        'selected_type':selected_type
                    }
                )

            messages.success(request, "Product added successfully")
            return redirect(request.path)


    else:
        form = ProductForm()

    return render(request, 'products/select_product_type.html', {
        'subcategory': subcategory,
        'types': types,
        'form': form,
        'selected_type':selected_type
    })


from django.contrib import messages

@login_required
def edit_product(request, id):

    product = get_object_or_404(Product,id=id, seller=request.user )

    if request.method == 'POST':

        form = ProductForm(request.POST,instance=product)
        '''in instance it take old value automatically so we can update it exist value'''

        images = request.FILES.getlist('images')

        # ✅ max 5 images
        if len(images) > 5:
            form.add_error(None, "Maximum 5 images allowed")

        if form.is_valid():

            form.save()

            ''' if new images uploaded'''
            if images:
                '''# delete old images'''
                product.images.all().delete()

                '''add new images'''
                for img in images:
                    ProductImage.objects.create(
                        product=product,
                        image=img
                    )

            messages.success(request, "Product updated successfully")

            return redirect('seller_dashboard')

    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, seller=request.user)

    product.delete()
    return redirect('seller_dashboard')

def product_detail(request, id):

    product = get_object_or_404( 
        Product,
        id=id
    )

    return render(request, 'products/product_detail.html',{'product': product})

# @login_required
# def add_to_wishlist(request,id):

#     product=get_object_or_404(Product, id=id)

#     Wishlist.objects.get_or_create(
#         user=request.user,
#         product=product
#     )
#     messages.success('request','Product Added In Wishlist')

#     return redirect('wishlist')


# @login_required
# def wishlist(request):

#     wishlist_items=Wishlist.objects.filter(
#         user=user.request
#     )

#     return render(request,'products/wishlist.html',{'wishlist_items':wishlist_items})

