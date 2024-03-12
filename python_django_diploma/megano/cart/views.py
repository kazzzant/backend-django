from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shopapp.models import Product

from .cart import Cart
from .models import Order, OrderItems
from .serializers import CartSerializer, OrderSerializer


def products_in_cart(cart):
    products = Product.objects.filter(id__in=cart.cart.keys())
    serializer = CartSerializer(products, many=True, context=cart.cart)
    return serializer.data


def update_count_in_cart(request, cart, add=1):
    product_id = request.data.get("id")
    if Product.objects.filter(id=product_id).exists():
        cart.add(item_id=product_id, count=add * request.data.get("count"))
    else:
        cart.remove(product_id)


class BasketView(APIView):
    def get(self, request):
        cart = Cart(request)
        return Response(products_in_cart(cart))

    def post(self, request):
        cart = Cart(request)
        update_count_in_cart(request, cart)
        return Response(products_in_cart(cart))

    def delete(self, request):
        cart = Cart(request)
        update_count_in_cart(request, cart, -1)
        return Response(products_in_cart(cart))


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(user_id=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        products = Product.objects.filter(id__in=[item["id"] for item in request.data])
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    fullName=request.user.profile.fullName,
                    email=request.user.profile.email,
                    phone=request.user.profile.phone,
                    totalCost=sum(
                        item["count"] * item["price"] for item in request.data
                    ),
                )
                order.products.set(products)
                for item in request.data:
                    (
                        OrderItems.objects.filter(
                            order_id=order.pk, product_id=item["id"]
                        ).update(price=item["price"], count=item["count"])
                    )
                data = {"orderId": order.pk}
                return Response(data)
        except Exception as ex:
            print("ERROR:", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        queryset = Order.objects.get(pk=id)
        serializer = OrderSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, id):
        try:
            with transaction.atomic():
                order = Order.objects.get(pk=id)
                data = request.data
                order.fullName = data["fullName"]
                order.phone = data["phone"]
                order.email = data["email"]
                order.deliveryType = data["deliveryType"]
                order.city = data["city"]
                order.address = data["address"]
                order.paymentType = data["paymentType"]
                order.status = data["status"]
                if data["deliveryType"] == "express":
                    order.deliveryCost = 500
                else:
                    if order.totalCost < 2000:
                        order.deliveryCost = 200
                    else:
                        order.deliveryCost = 0
                order.save()
                Cart(request).clear()
                data = {"orderId": order.pk}
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print("ERROR:", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentView(APIView):
    def post(self, request, id):
        order = Order.objects.get(pk=id)
        order.status = "Оплачен"
        order.save()
        return Response(status=status.HTTP_200_OK)
