from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("verify/", views.UserRegisterVerifyView.as_view(), name="user_register_verify"),
    path("logout/", views.UserLogOutView.as_view(), name="user_logout"),
    path("login/", views.UserLogInView.as_view(), name="user_login"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
]
