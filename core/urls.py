from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
]