from django.contrib import admin

# Register your models here.

from .models import Brand, Category

admin.site.register(Brand)
admin.site.register(Category)