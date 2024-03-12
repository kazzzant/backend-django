from django.urls import path

from .views import BasketView, OrderDetailView, OrdersView, PaymentView

urlpatterns = [
    path("basket", BasketView.as_view(), name="basket"),
    path("orders", OrdersView.as_view(), name="order_list"),
    path("order/<int:id>", OrderDetailView.as_view(), name="order"),
    path("payment/<int:id>", PaymentView.as_view(), name="payment"),
]
