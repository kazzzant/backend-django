# from django.shortcuts import render
import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Avatar, Profile
from .serializers import ChangePasswordSerializer, ProfileSerializer

User = get_user_model()


class SignInView(APIView):
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password)
                avatar_user = Avatar.objects.create()
                Profile.objects.create(
                    user=user, fullName=name, avatar_id=avatar_user.id
                )
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            print("Error:", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sign_out(request):
    logout(request)
    return HttpResponse(status=200)
    # return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("ERROR", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("currentPassword")):
                print("ERROR: wrong currentPassword")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("newPassword"))
            user.save()
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAvatarView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        instance = Avatar(src=request.FILES["avatar"])
        profile = request.user.profile
        profile.avatar = instance
        profile.avatar.save()
        profile.save()
        return Response(status=status.HTTP_200_OK)
