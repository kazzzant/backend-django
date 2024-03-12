from django.contrib import admin

from .models import (Category, CategoryImage, Product, ProductImage, Review,
                     Sale, Specification, Tag)

admin.site.register(CategoryImage)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Tag)
admin.site.register(Specification)
admin.site.register(Review)
admin.site.register(Sale)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "title", "parent", "image"
    list_display_links = "id", "title"
