from django.contrib.auth.models import User
from django.db import models

from shopapp.models import Product


class Order(models.Model):
    DELIVERY_TYPE = [("ordinary", "ordinary"), ("express", "express")]
    PAYMENT_TYPE = [("online", "online"), ("someone", "someone")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="orders",
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    fullName = models.CharField(default="", max_length=128, verbose_name="Полное имя")
    email = models.EmailField(default="", max_length=128, verbose_name="e-mail")
    phone = models.PositiveIntegerField(default="", verbose_name="телефон")
    deliveryType = models.CharField(
        max_length=64,
        choices=DELIVERY_TYPE,
        default="ordinary",
        verbose_name="тип доставки",
    )
    paymentType = models.CharField(
        max_length=64, choices=PAYMENT_TYPE, default="online", verbose_name="тип оплаты"
    )
    totalCost = models.DecimalField(
        max_digits=10, default=0, decimal_places=2, verbose_name="сумма заказа"
    )
    deliveryCost = models.DecimalField(
        max_digits=10, default=0, decimal_places=2, verbose_name="стоимость доставки"
    )
    status = models.CharField(max_length=64, default="new", verbose_name="статус")
    city = models.CharField(max_length=128, default="", verbose_name="город")
    address = models.CharField(max_length=256, default="", verbose_name="адрес")
    products = models.ManyToManyField(
        Product, through="OrderItems", related_name="orders"
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"({self.pk}) {self.fullName}: {self.city}, {self.address} - ({self.status})"


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    count = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "продукты в заказе"
        verbose_name_plural = "продукты в заказе"
