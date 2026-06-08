"""
URL configuration for drf_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from api.brand.views import BrandDetail, BrandList
from api.category.views import CategoryDetail, CategoryList
from api.product.views import (
    ProductDetail,
    ProductList,
    ProductVariantDetail,
    ProductVariantList,
)
from api.user.auth_views import LoginView, LogoutView, MeView, RefreshTokenView
from api.user.views import (
    UserAddressDetail,
    UserAddressList,
    UserDetail,
    UserList,
)
from api.cart.views import CartDetail, CartList, CartItemDetail, CartItemList
from api.voucher.views import VoucherDetail, VoucherList
from api.order.views import OrderDetail, OrderList, OrderItemDetail, OrderItemList
from api.payment.views import PaymentDetail, PaymentFundIn, PaymentList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login', LoginView.as_view()),
    path('auth/logout', LogoutView.as_view()),
    path('auth/refresh', RefreshTokenView.as_view()),
    path('auth/me', MeView.as_view()),
    path('brand', BrandList.as_view()),
    path('brand/<int:pk>', BrandDetail.as_view()),
    path('category', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('user', UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view()),
    path('user-address', UserAddressList.as_view()),
    path('user-address/<int:pk>', UserAddressDetail.as_view()),
    path('product', ProductList.as_view()),
    path('product/<int:pk>', ProductDetail.as_view()),
    path('product-variant', ProductVariantList.as_view()),
    path('product-variant/<int:pk>', ProductVariantDetail.as_view()),
    path('cart', CartList.as_view()),
    path('cart/<int:pk>', CartDetail.as_view()),
    path('cart-item', CartItemList.as_view()),
    path('cart-item/<int:pk>', CartItemDetail.as_view()),
    path('voucher', VoucherList.as_view()),
    path('voucher/<int:pk>', VoucherDetail.as_view()),
    path('order', OrderList.as_view()),
    path('order/<int:pk>', OrderDetail.as_view()),
    path('order-item', OrderItemList.as_view()),
    path('order-item/<int:pk>', OrderItemDetail.as_view()),
    path('payment', PaymentList.as_view()),
    path('payment/<int:pk>', PaymentDetail.as_view()),
    path('payment/<int:pk>/fund-in', PaymentFundIn.as_view()),
]
