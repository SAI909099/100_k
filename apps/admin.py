from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from django.utils.html import format_html

from apps.models import Category, ProductImage, Product, Order, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = 'slug',

    @admin.display(empty_value="?")
    def product_count(self, obj):
        return obj.products.count()


class ProductImageInline(StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ("slug", "owner",)
    inlines = [ProductImageInline]

    @admin.display(empty_value="?")
    def is_exists(self, obj):
        icon_url = 'https://img.icons8.com/?size=100&id=9fp9k4lPT8us&format=png&color=000000'
        if not obj.quantity:
            icon_url = 'https://img.icons8.com/?size=100&id=63688&format=png&color=000000'
        return format_html("<img src='{}' style='width: 30px' />", icon_url)

    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratish
            obj.owner = request.user
        obj.save()



