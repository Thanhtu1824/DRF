"""
Permission classes:
  Is*  — role (IsAdmin, IsStaff, …) or ownership (IsOwner)
  Can* — business capability (CanBuy, CanSell, …)
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from api.order.access import user_may_access_order, user_may_write_order


def current_user(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    return None


def is_read_only_method(request):
    return request.method in SAFE_METHODS


def user_can_manage_back_office(request):
    user = current_user(request)
    if user is None:
        return False
    return user.can_manage_back_office()


def owner_user_id(obj, owner_field):
    value = obj
    for part in owner_field.split('.'):
        value = getattr(value, part)
    return value.pk if hasattr(value, 'pk') else value


def product_seller_id(obj):
    if hasattr(obj, 'seller_id'):
        return obj.seller_id
    return obj.product.seller_id


def _seller_owns_product(user, obj):
    if user.can_manage_back_office():
        return True
    if user.is_seller_role():
        return product_seller_id(obj) == user.pk
    return False


# ---- Is* — role or ownership ----


class IsAdmin(BasePermission):
    message = 'Only admin can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        return user is not None and user.is_admin_role()


class IsStaff(BasePermission):
    message = 'Only staff can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        return user is not None and user.is_staff_role()


class IsSeller(BasePermission):
    message = 'Only seller can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        return user is not None and user.is_seller_role()


class IsCustomer(BasePermission):
    message = 'Only customer can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        return user is not None and user.is_customer_role()


class IsOwner(BasePermission):
    message = 'You can only access your own resources.'

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        owner_field = getattr(view, 'owner_field', 'user')
        return owner_user_id(obj, owner_field) == user.pk


class CanAccessUser(BasePermission):
    message = 'This profile belongs to another user.'

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        if user.is_admin_role():
            return True
        return obj.pk == user.pk


class RegisterPublic(IsAdmin):
    """POST /user is public; GET list requires IsAdmin."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)


# ---- Can* — business capability ----


class CanBuy(BasePermission):
    message = 'Only buyer accounts can use this feature.'

    def has_permission(self, request, view):
        user = current_user(request)
        return user is not None and user.can_buy()


class CanSell(BasePermission):
    message = 'You do not have permission to manage the catalog.'

    def has_permission(self, request, view):
        if is_read_only_method(request):
            return True
        user = current_user(request)
        return user is not None and user.can_sell()

    def has_object_permission(self, request, view, obj):
        if is_read_only_method(request):
            return True
        user = current_user(request)
        if user is None:
            return False
        return _seller_owns_product(user, obj)


class CanManageBackOffice(BasePermission):
    message = 'Only back-office roles can perform this action.'

    def has_permission(self, request, view):
        if is_read_only_method(request):
            return True
        user = current_user(request)
        return user is not None and user.can_manage_back_office()


class CanOrder(BasePermission):
    message = 'You do not have permission to access this order.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        if request.method == 'POST':
            return user.can_buy()
        if user.can_intervene_orders():
            return True
        if user.can_fulfill_orders():
            return True
        if user.can_buy():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        order = obj.order if hasattr(obj, 'order_id') else obj
        if not user_may_access_order(user, order):
            return False
        if is_read_only_method(request):
            return True
        return user_may_write_order(user, order)


class CanAccessPayment(CanBuy):
    message = 'You can only access your own payments.'

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None or not user.can_buy():
            return False
        return obj.order.user_id == user.pk
