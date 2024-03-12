from django.urls import path

from .views import (ChangeAvatarView, ChangePasswordView, ProfileView,
                    SignInView, SignUpView, sign_out)

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-out", sign_out),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", ChangePasswordView.as_view(), name="password"),
    path("profile/avatar", ChangeAvatarView.as_view(), name="avatar"),
]
