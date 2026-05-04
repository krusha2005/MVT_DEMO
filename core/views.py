from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')


def seller_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'seller':
        return redirect('home')

    return render(request, 'seller/dashboard.html')