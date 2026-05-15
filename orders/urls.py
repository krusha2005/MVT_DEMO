from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('place-order/',views.place_order,name='place_order'),
    path('buy_now/<int:id>/',views.buy_now,name='buy_now'),
    path('seller/orders/',views.seller_orders, name='seller_orders'),
    path('seller/order/<int:id>/',views.seller_order_detail, name='seller_order_detail'),
    path('seller/order/status/<int:id>/',views.update_order_status, name='update_order_status'),
]
