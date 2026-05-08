from django.urls import path
from . import views

urlpatterns=[
    path('wishlist/add/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wish/<int:id>/',views.remove_wish,name='remove_wish'),
]