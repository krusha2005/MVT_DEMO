from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart'),
    path('increase/<int:id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease/<int:id>/',views.decrease_quantity,name='decrease_quantity'),
    path('remove/<int:id>/',views.remove_cart_item,name='remove_cart_item'),

]