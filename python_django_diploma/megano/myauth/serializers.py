from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(required=False)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def update(self, instance, validated_data):
        avatar_data = validated_data.pop("avatar")
        avatar = instance.avatar

        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        # instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        avatar.src = avatar_data.get("src", avatar.src)
        avatar.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
