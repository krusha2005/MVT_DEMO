from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ProductImageForm, CategoryForm, SubCategoryForm, ProductTypeForm
from .models import Category, SubCategory, ProductType, ProductImage
from cart.models import CartItem
from django.contrib import messages
from products.models import Product
from django.core.exceptions import ValidationError
from wishlist.models import Wishlist


# def add_category(request):
#     form = CategoryForm(request.POST or None, request.FILES or None)

#     if form.is_valid():
#         form.save()
#         return redirect('category_list')

#     return render(request, 'category/add.html', {'form': form})

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

    '''for delete '''
    product.is_deleted = True

    product.save()

    # for wishlist
    Wishlist.objects.filter( product = product).delete()

    messages.success(request,'product deleted successfully!')

    return redirect('seller_dashboard')

def product_detail(request, id):

    product = get_object_or_404(
        Product.objects.select_related(
            'seller__seller_profile',
            'category',
            'product_type'
        ).prefetch_related(
            'images'
        ),
        id = id,
        is_deleted = False
    )

    return render(request, 'products/product_detail.html',{'product': product})


'''add catgory from admin nd edit nd show all category '''
def category_list(request):

    categories = Category.objects.all()
    # category_form = CategoryForm()

    edit_id= request.GET.get('edit')

    if edit_id:
        category = Category.objects.get(id=edit_id)
        category_form =  CategoryForm(
            instance=category
            )
    else:
        category_form = CategoryForm()
        
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')

        if edit_id:
            category = Category.objects.get(id= edit_id)
            category_form = CategoryForm(
                request.POST,
                request.FILES,
                instance=category
            )

        else:
            category_form =  CategoryForm(
                request.POST,
                request.FILES
            )

        if category_form.is_valid():
            category_form.save()
            return redirect('category_list')

    return render(request,'dashboard/categories.html',{ 
        'categories' : categories,
        'category_form': category_form,
        'edit_id': edit_id
        })

def delete_category(request, id):
    category = get_object_or_404(
        Category,
        id = id
    )
    category.delete()
    return redirect('category_list')

'''add subcategory form category view nd also edit nd delete subcatgory'''
def subcategory_list(request, id):

    category = get_object_or_404(
        Category,
        id = id
    )

    subcategories = SubCategory.objects.filter(
        category = category
    )
    edit_sub_id = request.GET.get('edit_sub')

    subcategory_form = SubCategoryForm()

    if edit_sub_id:
        subcategory = SubCategory.objects.get(id=edit_sub_id)
        subcategory_form = SubCategoryForm(
            instance=subcategory
        )
    else:
        subcategory_form = SubCategoryForm()

    if request.method == 'POST':
        edit_sub_id = request.POST.get('edit_sub_id')

        if edit_sub_id:
            subcategory = SubCategory.objects.get(id=edit_sub_id)
            subcategory_form=SubCategoryForm(
                request.POST,
                request.FILES,
                instance=subcategory
                )
        else:
            subcategory_form = SubCategoryForm(
                request.POST,
                request.FILES
            )

        if subcategory_form.is_valid():
            '''commit=false bcoz it save temp object not direct in db so we can add before FK like in this we attach catgory to subcategory'''
            subcategory = subcategory_form.save(
                commit= False
            )
            subcategory.category = category
            subcategory.save()

            return redirect('subcategory_list',id=category.id)
        
    return render(request,'dashboard/subcategory_list.html',{
        'category' : category,
        'subcategories' : subcategories,
        'subcategory_form' : subcategory_form,
        'edit_sub_id' : edit_sub_id
    })

def delete_subcategory(request, id):

    subcategory = get_object_or_404(
        SubCategory,
        id = id
    )
    '''category_id use bcoz after delete subcategory is deleted so using category id redirect page '''
    category_id = subcategory.category.id
    subcategory.delete()
    return redirect('subcategory_list',id=category_id)

'''productType for add from subcategory view foo speific subcat add productTypes nd also edit'''
def productType_list(request, id):

    subcategory = get_object_or_404(
        SubCategory,
        id = id
    )

    productTypes = ProductType.objects.filter(
        subcategory = subcategory
    )

    edit_id = request.GET.get('edit')
    productType_form = ProductForm()

    if edit_id:
        productType = ProductType.objects.get(id=edit_id)
        productType_form = ProductTypeForm(
            instance=productType
        )

    else:
        productType_form = ProductTypeForm()

    if request.method == 'POST':
        edit_id =request.POST.get('edit_id')

        if edit_id:
            productType = ProductType.objects.get(id=edit_id)
            productType_form = ProductTypeForm(
                request.POST,
                request.FILES,
                instance=productType
            )
        else:
            productType_form = ProductTypeForm(
                request.POST,
                request.FILES
            )

        if productType_form.is_valid():
            productType = productType_form.save(
                commit=False
            )
            productType.subcategory = subcategory
            productType.save()

            return redirect('productType_list',id=subcategory.id)
    
    return render(request,'dashboard/productType_list.html',{
        'subcategory' : subcategory,
        'productTypes' : productTypes,
        'productType_form' : productType_form,
        'edit_id' : edit_id
    })


def delete_productType(request, id):
    productType = get_object_or_404(
        ProductType,
        id = id
    )
    subcategory_id = productType.subcategory.id
    productType.delete()

    return redirect('productType_list',id=subcategory_id)