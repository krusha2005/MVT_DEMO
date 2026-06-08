from celery import shared_task
from cart.models import Cart

@shared_task
def cart_reminder():
    carts = Cart.objects.filter(
        items__isnull = False
    ).prefetch_related(
        'items__product'
    ).distinct()

    for cart in carts:
        item_msg = " "

        for item in cart.items.all():
            item_msg += f"{item.product.name} {item.product.price}"

        msg = f"dear {cart.user.username} please place your order {item_msg}"
        print(msg)

        