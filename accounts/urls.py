from django.urls import path
from . import views

urlpatterns = [
    path('buyer-register/', views.buyer_register, name='buyer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('seller-register/', views.seller_register, name='seller_register'),
    path('register/', views.register_choice, name='register_choice'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/out_of_stock/',views.out_of_stock, name='out_of_stock'),
    path('seller/deleted_products/',views.deleted_products, name='deleted_products'),
    path('seller/deleted_product_buyers/<int:id>/',views.deleted_product_buyers, name='deleted_product_buyers'),
    path('admin/admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/admin-seller-detail/<int:id>/',views.admin_seller_detail, name='admin_seller_detail'),
    path('admin/delete-seller/<int:id>/',views.delete_seller, name='delete_seller'),
    path('admin/delete-buyer/<int:id>/',views.delete_buyer, name='delete_buyer'),
    path('admin/admin-buyer-detail/<int:id>/',views.admin_buyer_detail, name='admin_buyer_detail'),
]
