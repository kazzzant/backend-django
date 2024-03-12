# from django.shortcuts import render
from datetime import date

from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Review, Sale, Tag
from .serializers import (CatalogSerializer, CategorySerializer,
                          ProductSerializer, ReviewSerializer, SaleSerializer,
                          TagSerializer)


def filter_catalog(request):
    """Фильтр каталога продуктов"""
    filter_items = {}
    title = request.query_params.get("filter[name]")
    if title:
        filter_items["title__icontains"] = title
    min_price = request.query_params.get("filter[minPrice]")
    max_price = request.query_params.get("filter[maxPrice]")
    if min_price:
        filter_items["price__range"] = (min_price, max_price)
    available = request.query_params.get("filter[available]")
    if available == "true":
        filter_items["count__gt"] = 0
    free_delivery = request.query_params.get("filter[freeDelivery]")
    if free_delivery:
        filter_items["freeDelivery"] = free_delivery.capitalize()
    tags = request.query_params.getlist("tags[]")
    if tags:
        filter_items["tags__id__in"] = tags
    category_id = int(request.GET.get("category", 0))
    if Category.objects.filter(id=category_id).exists():
        filter_items["category__id"] = category_id

    return filter_items


def order_catalog(request):
    sort = request.GET.get("sort")
    sort_type = request.GET.get("sortType")
    sort_type = "-" if sort_type == "inc" else ""
    if sort:
        return f"{sort_type}{sort}"
    return "id"


class CategoryView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class CatalogView(APIView):
    def get(self, request):
        filter_items = filter_catalog(request)
        sort = order_catalog(request)
        product = Product.objects.filter(**filter_items).order_by(sort).distinct()
        serializer = CatalogSerializer(product, many=True)
        paginator = Paginator(serializer.data, 20)
        page = request.GET.get("currentPage", 1)
        page_obj = paginator.get_page(page)
        return Response(
            {
                "items": page_obj.object_list,
                "currentPage": page,
                "lastPage": paginator.num_pages,
            }
        )


class ProductView(APIView):
    def get(self, request, id):
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ReviewView(APIView):
    def post(self, request, id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product_id=id)
            return Response(serializer.data)
        else:
            print("ERROR", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SaleView(APIView):
    def get(self, request):
        current_date = date.today()
        queryset = Sale.objects.filter(
            dateFrom__lte=current_date, dateTo__gte=current_date
        )
        serializer = SaleSerializer(queryset, many=True)
        paginator = Paginator(serializer.data, 20)
        page = request.GET.get("currentPage", 1)
        page_obj = paginator.get_page(page)
        return Response(
            {
                "items": page_obj.object_list,
                "currentPage": page,
                "lastPage": paginator.num_pages,
            }
        )


class BannerView(ListAPIView):
    queryset = Product.objects.order_by("price", "id")[:8]
    serializer_class = CatalogSerializer


class PopularView(ListAPIView):
    queryset = (
        Product.objects.annotate(reviews_count=Count("reviews"))
        .filter(reviews_count__gte=1)
        .order_by("-reviews_count", "id")
    )[:8]
    serializer_class = CatalogSerializer


class LimitedView(ListAPIView):
    queryset = Product.objects.filter(count__lte=8).order_by("count", "id")[:16]
    serializer_class = CatalogSerializer
