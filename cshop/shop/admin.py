from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop.models import Product, Category


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
