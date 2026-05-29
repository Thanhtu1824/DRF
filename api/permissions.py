"""
API permissions.

Rules live on User (is_admin_role, is_staff_or_admin_role, …).
Each class below maps to one clear rule for views.
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission


def _current_user(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    return None


def _is_read_only(request):
    return request.method in SAFE_METHODS


def _product_seller_id(obj):
    if hasattr(obj, 'seller_id'):
        return obj.seller_id
    return obj.product.seller_id


# ---- Who is calling? (view level) ----


class IsAdminRole(BasePermission):
    message = 'Only admin can perform this action.'

    def has_permission(self, request, view):
        user = _current_user(request)
        return user is not None and user.is_admin_role()


class IsStaffRole(BasePermission):
    message = 'Only staff can perform this action.'

    def has_permission(self, request, view):
        user = _current_user(request)
        return user is not None and user.is_staff_role()


class IsStaffOrAdmin(BasePermission):
    message = 'Only staff or admin can perform this action.'

    def has_permission(self, request, view):
        user = _current_user(request)
        return user is not None and user.is_staff_or_admin_role()


class IsSellerRole(BasePermission):
    message = 'Only seller can perform this action.'

    def has_permission(self, request, view):
        user = _current_user(request)
        return user is not None and user.is_seller_role()


# ---- Does this row belong to the caller? (object level) ----


class IsOwner(BasePermission):
    """
    Set view.owner_field = 'user' when the model has a user FK.
    For User rows, leave owner_field unset.
    """

    message = 'You can only access your own resources.'

    def has_object_permission(self, request, view, obj):
        user = _current_user(request)
        if user is None:
            return False

        owner_field = getattr(view, 'owner_field', None)
        if owner_field:
            owner = getattr(obj, owner_field)
            owner_id = owner.pk if hasattr(owner, 'pk') else owner
            return owner_id == user.pk

        return obj.pk == user.pk


class CanAccessUserProfile(BasePermission):
    """User profile: admin any user; others only their own row."""

    message = 'This profile belongs to another user.'

    def has_object_permission(self, request, view, obj):
        user = _current_user(request)
        if user is None:
            return False
        if user.is_admin_role():
            return True
        return obj.pk == user.pk


def any_of(*permission_classes, message=None):
    """Pass when at least one permission passes."""

    class _Combined(BasePermission):
        def has_permission(self, request, view):
            return any(
                p().has_permission(request, view) for p in permission_classes
            )

        def has_object_permission(self, request, view, obj):
            return any(
                p().has_object_permission(request, view, obj)
                for p in permission_classes
            )

    if message:
        _Combined.message = message
    return _Combined


# ---- Catalog: brand, category, product, voucher ----


class ReadOnlyOrStaffOrAdmin(BasePermission):
    """GET (and other safe methods): public. POST/PUT/DELETE: staff or admin."""

    message = 'Only staff or admin can perform this action.'

    def has_permission(self, request, view):
        if _is_read_only(request):
            return True
        user = _current_user(request)
        return user is not None and user.is_staff_or_admin_role()


class CanManageCatalog(BasePermission):
    """Create or update catalog items."""

    message = 'Only seller, staff, or admin can manage catalog items.'

    def has_permission(self, request, view):
        user = _current_user(request)
        if user is None:
            return False
        return user.is_seller_role() or user.is_staff_or_admin_role()


class IsProductOwnerOrStaffOrAdmin(BasePermission):
    """Write product/variant: staff/admin for all; seller for own products only."""

    message = 'Only the product seller, staff, or admin can perform this action.'

    def has_permission(self, request, view):
        if _is_read_only(request):
            return True
        user = _current_user(request)
        if user is None:
            return False
        return user.is_seller_role() or user.is_staff_or_admin_role()

    def has_object_permission(self, request, view, obj):
        if _is_read_only(request):
            return True

        user = _current_user(request)
        if user is None:
            return False

        if user.is_staff_or_admin_role():
            return True

        if user.is_seller_role():
            return _product_seller_id(obj) == user.pk

        return False
