from django.contrib import admin

# Register your models here.
from goods.models import Categories, Products, ProductImage

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_display = ('name', 'quantity', 'price', 'discount', 'category')
    list_editable = ('quantity', 'price', 'discount')
    search_fields = ['name', 'description']
    list_filter = ('category', 'discount', 'quantity')
    fields = ['name', 'category', 'slug', 'description', ('price', 'discount'), 'quantity']