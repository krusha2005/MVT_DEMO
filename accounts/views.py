from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import SellerProfile, User
from .forms import LoginForm, BuyerRegisterForm, SellerRegisterForm
from django.contrib import messages

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


# for login for buyer nd seller both
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔥 role-based redirect
            if user.role == 'buyer':
                return redirect('home')
            elif user.role == 'seller':
                return redirect('seller_dashboard')

        else:
            messages.error(request, "Invalid username or password")  # ✅

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

# def seller_register(request):
#     if request.method == 'POST':
#         form = SellerRegisterForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)

#             # IMPORTANT: set password BEFORE saving user
#             password = form.cleaned_data.get('password')
#             user.set_password(password)

#             user.role = 'seller'
#             user.save()

#             # save seller profile
#             seller_profile = SellerProfile.objects.create(user=user)
#             categories = form.cleaned_data.get('categories')
#             if categories:
#                 seller_profile.categories.set(categories)

#             messages.success(request, "Seller account created successfully")

#             return redirect('login')

#     else:
#         form = SellerRegisterForm()

#     return render(request, 'accounts/seller_register.html', {'form': form})