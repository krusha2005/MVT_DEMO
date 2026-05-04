from django.urls import path
from . import views

urlpatterns = [
    path('buyer-register/', views.buyer_register, name='buyer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
]