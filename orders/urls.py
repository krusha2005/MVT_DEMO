from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('place-order/',views.place_order,name='place_order'),
    path('buy_now/<int:id>/',views.buy_now,name='buy_now')
]