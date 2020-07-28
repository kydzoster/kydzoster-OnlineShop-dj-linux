from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # value is automatically set using the value from other fields (name), this is for generating slug
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # this will allow to edit multiple rows from the list_display field
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
