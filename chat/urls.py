from django.urls import path
from .views import start_chat, chat_room, seller_chat_list

urlpatterns = [
    path("start-chat/<int:product_id>/",start_chat,name="start-chat"),
    path("room/<int:room_id>/",chat_room,name="chat-room"),
    path("seller-chat-list/",seller_chat_list,name="seller-chat-list"),
]