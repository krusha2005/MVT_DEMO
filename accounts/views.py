from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, BuyerRegisterForm
from django.contrib import messages



def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'buyer'
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()

            messages.success(request, "Account created successfully. Please login.")  
            return redirect('login')   # we will create login next
          
    else:
        form = BuyerRegisterForm()

    return render(request, 'accounts/buyer_register.html', {'form': form})


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