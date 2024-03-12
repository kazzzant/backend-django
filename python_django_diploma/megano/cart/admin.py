from django.contrib import admin

from .models import Order, OrderItems


class OrderItemInline(admin.TabularInline):
    model = OrderItems


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)


admin.site.register(Order, OrderAdmin)
