from django.urls import include, path
from . import views


app_name = 'accounts'

admin_paths = [
    path("showusers/",views.AdminShowUserView.as_view(),name="admin_show_user"),
    path("delete/<int:user_id>",views.AdminUserDeleteView.as_view(),name="admin_delete_user")
]

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("verify/", views.UserRegisterVerifyView.as_view(), name="user_register_verify"),
    path("logout/", views.UserLogOutView.as_view(), name="user_logout"),
    path("login/", views.UserLogInView.as_view(), name="user_login"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("profileEdit/", views.UserProfileEditView.as_view(), name="user_profile_edit"),
    path("admin/",include(admin_paths))
]



