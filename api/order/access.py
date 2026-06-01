"""Order visibility and access helpers (buyer, seller fulfillment, staff).

Orders are never hard-deleted via API; cancel with status=cancelled on update.
"""

from django.db.models import Q

from api.order.models import Order, OrderItem


def order_has_seller_products(order, seller_id):
    return order.items.filter(product__seller_id=seller_id).exists()


def orders_queryset_for(user):
    if user is None:
        return Order.objects.none()
    if user.can_intervene_orders():
        return Order.objects.all()
    if user.can_view_seller_orders():
        return Order.objects.filter(
            items__product__seller_id=user.pk,
        ).distinct()
    if user.can_shop_as_buyer():
        return Order.objects.filter(user=user)
    return Order.objects.none()


def order_items_queryset_for(user):
    if user is None:
        return OrderItem.objects.none()
    if user.can_intervene_orders():
        return OrderItem.objects.all()
    if user.can_view_seller_orders():
        return OrderItem.objects.filter(product__seller_id=user.pk)
    if user.can_shop_as_buyer():
        return OrderItem.objects.filter(order__user=user)
    return OrderItem.objects.none()


def user_may_access_order(user, order):
    if user is None:
        return False
    if user.can_intervene_orders():
        return True
    if user.can_shop_as_buyer() and order.user_id == user.pk:
        return True
    if user.can_view_seller_orders() and order_has_seller_products(order, user.pk):
        return True
    return False


def user_may_write_order(user, order):
    if user is None:
        return False
    if user.can_intervene_orders():
        return True
    if user.can_shop_as_buyer() and order.user_id == user.pk:
        return True
    return False
