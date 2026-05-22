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
from api.brand.views import BrandList, BrandDetail
from api.category.views import CategoryList, CategoryDetail

urlpatterns = [

    path('admin/', admin.site.urls),
    path('brand/', BrandList.as_view()),
    path('brand/<int:pk>', BrandDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),

]
