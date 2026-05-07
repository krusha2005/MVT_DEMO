from django.urls import path
from . import views

urlpatterns = [
    path('buyer-register/', views.buyer_register, name='buyer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('seller-register/', views.seller_register, name='seller_register'),
    path('register/', views.register_choice, name='register_choice'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    
]