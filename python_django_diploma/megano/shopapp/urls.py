from django.urls import path

from .views import (BannerView, CatalogView, CategoryView, LimitedView,
                    PopularView, ProductView, ReviewView, SaleView, TagView)

urlpatterns = [
    path("categories", CategoryView.as_view(), name="categories"),
    path("catalog", CatalogView.as_view(), name="catalog"),
    path("tags", TagView.as_view(), name="tag"),
    path("sales", SaleView.as_view(), name="sale"),
    path("banners", BannerView.as_view(), name="banners"),
    path("products/limited", LimitedView.as_view(), name="limited"),
    path("products/popular", PopularView.as_view(), name="popular"),
    path("product/<int:id>", ProductView.as_view(), name="product_view"),
    path("product/<int:id>/reviews", ReviewView.as_view(), name="reviews"),
]
