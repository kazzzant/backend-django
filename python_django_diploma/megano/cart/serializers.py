from datetime import date

from django.db.models import Avg, Count
from rest_framework import serializers

from shopapp.models import Product
from shopapp.serializers import ProductImageSerializer, TagSerializer

from .models import Order


class CartSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)
    count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_count(self, obj):
        return self.context.get(str(obj.pk)).get("count")

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return reviews.aggregate(Count("id"))["id__count"]
        return 0

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)
        return 0

    def get_price(self, obj):
        current_date = date.today()
        price = obj.sales.values("salePrice").filter(
            dateFrom__lte=current_date, dateTo__gte=current_date
        )
        if price.exists():
            return price[0]["salePrice"]
        return obj.price


class OrderProductsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return reviews.aggregate(Count("id"))["id__count"]
        return 0

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)
        return 0

    def get_price(self, obj):
        data = obj.order_items.values("price").filter(product_id=obj.id)
        return data[0]["price"]

    def get_count(self, obj):
        data = obj.order_items.values("count").filter(product_id=obj.id)
        return data[0]["count"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True)
    createdAt = serializers.SerializerMethodField()
    totalCost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_createdAt(self, obj):
        return obj.createdAt.strftime("%Y-%m-%e %H:%M")

    def get_totalCost(self, obj):
        return obj.totalCost + obj.deliveryCost
