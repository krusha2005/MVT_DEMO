from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from products.models import Product

# Create your views here.

def start_chat(request, product_id):

    product = get_object_or_404(
        Product,
        id = product_id
    )
    room,created = ChatRoom.objects.get_or_create(
        buyer = request.user,
        seller = product.seller,
        product = product
    )
    return redirect("chat-room",room.id)

def chat_room(request,room_id):

    room = get_object_or_404(
        ChatRoom,
        id = room_id
    )

    massages = room.messages.select_related(
        "sender"
    ).order_by("created_at")

    return render(request,'chat/chat_room.html',{
        "room":room,
        "msgs":massages,
    })


@login_required
def seller_chat_list(request):

    rooms = ChatRoom.objects.filter(
        seller=request.user
    ).select_related(
        "buyer",
        "product"
    )

    return render(
        request,
        "chat/seller_chat_list.html",
        {
            "rooms": rooms
        }
    )