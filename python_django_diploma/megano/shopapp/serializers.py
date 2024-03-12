from datetime import date

from django.db.models import Avg, Count
from rest_framework import serializers

from .models import (Category, CategoryImage, Product, ProductImage, Review,
                     Sale, Specification, Tag)


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = CategoryImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class SubCategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Category
        fields = ["id", "title", "image"]

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        if obj["image"] is None:
            obj["image"] = {"src": "#", "alt": ""}
        return obj


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    subcategories = SubCategorySerializer(required=False, many=True)

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        if obj["image"] is None:
            obj["image"] = {"src": "#", "alt": ""}
        return obj


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["name", "value"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)
    specifications = SpecificationSerializer(required=False, many=True)
    reviews = ReviewSerializer(required=False, many=True)
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
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

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


class CatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)
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


class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]

    def get_dateFrom(self, instance):
        return instance.dateFrom.strftime("%m-%e")

    def get_dateTo(self, instance):
        return instance.dateTo.strftime("%m-%e")

    def get_images(self, instance):
        images = []
        for image in instance.product.images.all():
            images.append({"src": image.src.url, "alt": image.alt})
        return images
