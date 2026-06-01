"""API permissions — use User.can_*() for business rules, is_*_role() for exact role."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


def current_user(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    return None


def is_read_only_method(request):
    return request.method in SAFE_METHODS


def user_can_access_back_office(request):
    user = current_user(request)
    if user is None:
        return False
    return user.can_access_back_office()


def user_can_manage_sales_catalog(request):
    user = current_user(request)
    if user is None:
        return False
    return user.can_manage_sales_catalog()


def customer_read_only_allows(request):
    """Safe methods: anyone. Mutations: BACK_OFFICE_ROLES."""
    if is_read_only_method(request):
        return True
    user = current_user(request)
    if user is None:
        return False
    return user.can_access_back_office()


def seller_catalog_write_allows(request):
    """Safe methods: anyone. Mutations: SALES_ROLES."""
    if is_read_only_method(request):
        return True
    user = current_user(request)
    if user is None:
        return False
    return user.can_manage_sales_catalog()


def seller_owns_product_object(user, obj):
    if user.can_access_back_office():
        return True
    if user.is_seller_role():
        return product_seller_id(obj) == user.pk
    return False


def owner_user_id(obj, owner_field):
    value = obj
    for part in owner_field.split('.'):
        value = getattr(value, part)
    return value.pk if hasattr(value, 'pk') else value


def product_seller_id(obj):
    if hasattr(obj, 'seller_id'):
        return obj.seller_id
    return obj.product.seller_id


# ---- Role (exact role) ----


class IsAdminRole(BasePermission):
    message = 'Only admin can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        return user.is_admin_role()


class IsStaffRole(BasePermission):
    message = 'Only staff can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        return user.is_staff_role()


class IsSellerRole(BasePermission):
    message = 'Only seller can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        return user.is_seller_role()


# ---- Business (can_*) ----


class CanAccessBackOffice(BasePermission):
    message = 'Only back-office roles can perform this action.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        return user.can_access_back_office()


# ---- Ownership ----


class IsOwner(BasePermission):
    message = 'You can only access your own resources.'

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        owner_field = getattr(view, 'owner_field', None)
        if owner_field:
            return owner_user_id(obj, owner_field) == user.pk
        return obj.pk == user.pk


class CanAccessUserProfile(BasePermission):
    message = 'This profile belongs to another user.'

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        if user.is_admin_role():
            return True
        return obj.pk == user.pk


class RegisterPublicAdminList(BasePermission):
    """POST register is public; GET list is admin only."""

    message = 'Only admin can perform this action.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user = current_user(request)
        if user is None:
            return False
        return user.is_admin_role()


class IsAuthenticatedOwner(BasePermission):
    message = 'You can only access your own resources.'

    def has_permission(self, request, view):
        return current_user(request) is not None

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        owner_field = getattr(view, 'owner_field', 'user')
        return owner_user_id(obj, owner_field) == user.pk


# ---- Catalog ----


class CustomerReadOnly(BasePermission):
    """
    Brand, category, voucher: read for all; write for BACK_OFFICE_ROLES.
    """

    message = 'Only back-office roles can modify this resource.'

    def has_permission(self, request, view):
        return customer_read_only_allows(request)


class SellerCanManageCatalog(BasePermission):
    """Product list: read for all; write for SALES_ROLES."""

    message = 'Only sales roles can manage catalog items.'

    def has_permission(self, request, view):
        return seller_catalog_write_allows(request)


class SellerOwnsProduct(BasePermission):
    """Product detail: read for all; write for back office or owning seller."""

    message = 'Only the product seller or back-office roles can perform this action.'

    def has_permission(self, request, view):
        return seller_catalog_write_allows(request)

    def has_object_permission(self, request, view, obj):
        if is_read_only_method(request):
            return True
        user = current_user(request)
        if user is None:
            return False
        return seller_owns_product_object(user, obj)


# ---- Payment ----


class CanAccessOwnPayment(BasePermission):
    message = 'You can only access your own payments.'

    def has_permission(self, request, view):
        return current_user(request) is not None

    def has_object_permission(self, request, view, obj):
        user = current_user(request)
        if user is None:
            return False
        return obj.order.user_id == user.pk


class BackOfficeFundIn(BasePermission):
    message = 'Only back-office roles can perform fund-in.'

    def has_permission(self, request, view):
        user = current_user(request)
        if user is None:
            return False
        return user.can_access_back_office()
