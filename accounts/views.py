import email
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.views import View
from django.contrib import messages
from accounts.forms import UserLogInForm, UserProfileEditForm, UserRegisterForm, UserRegisterVerifyForm
from accounts.models import RGScode
from .models import User
# from utils import send_rgs_code
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class UserRegisterView(View):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("todo:show_todos")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cl = form.cleaned_data
            # self.request.session["user_info"] = {
            #     "phone_number": cl["phone_number"],
            #     "email": cl["email"],
            #     "full_name": cl["full_name"],
            #     "password": cl["password"]
            # }
            user = User.objects.create_user(email=cl["email"], phone_number=cl["phone_number"],
                                                full_name=cl["full_name"], password=cl["password"])
            messages.success(request, f"{user.full_name} shoma sabt nam kardid", "success")
            # random_code = randint(0, 9999)
            # RGScode.objects.create(
            #     phone_number=cl["phone_number"], code=random_code)
            # send_rgs_code(cl["phone_number"],random_code)
            return redirect("accounts:user_login")
        # messages.success(request, f"{user.full_name} etelaat na motabar", "success")
        return render(request, self.template_name, {"form": form})





class UserLogInView(View):
    template_name = "accounts/login.html"
    form_class = UserLogInForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("todo:show_todos")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cl = form.cleaned_data
            user = authenticate(username=cl["email"], password=cl["password"])
            if user:
                login(request, user)
                messages.success(request, "khosh amadid", "success")
                return redirect("todo:show_todos")
            messages.error(request, "email ya pass eshteba ast", "danger")

        return render(request, self.template_name, {"form": form})


class UserLogOutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect("core:home")
# Create your views here.


class UserProfileView(LoginRequiredMixin, View):
    template_name = "accounts/user_profile.html"

    def get(self, request):
        return render(request, self.template_name)


class UserProfileEditView(LoginRequiredMixin, View):
    form_class = UserProfileEditForm
    template_name = "accounts/user_profile_edit.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class(instance=request.user)})

    def post(self, request):
        form = self.form_class(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            cl = form.cleaned_data
            user = form.save(commit=False)
            user.profile.img =cl["img"] if cl["img"] else user.profile.img
            user.profile.save()
            user.save()
            return redirect("accounts:user_profile")
        return render(request, self.template_name, {"form": form})


class AdminShowUserView(LoginRequiredMixin, View):
    template_name = "accounts/admin/show_users.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        return redirect("accounts:user_profile")

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {"users": users})


class AdminUserDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        return redirect("accounts:user_profile")

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            messages.success(request, " user delete shode !", "success")
            return redirect("accounts:admin_show_user")
        except User.DoesNotExist:
            messages.error(request, " user delete shode !", "danger")
            return redirect("accounts:admin_show_user")


class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = 'accounts/password_reset_form.html'
	success_url = reverse_lazy('accounts:password_reset_done')
	email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = 'accounts/password_reset_confirm.html'
	success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'accounts/password_reset_complete.html'





# class UserRegisterVerifyView(View):
#     form_class = UserRegisterVerifyForm
#     template_name = "accounts/verify_code.html"

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect("todo:show_todos")
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request):
#         context = {
#             "form": self.form_class
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data["code"]
#             try:
#                 user_info = request.session["user_info"]
#                 code = RGScode.objects.get(
#                     phone_number=user_info["phone_number"], code=code)
#                 user = User.objects.create_user(email=user_info["email"], phone_number=user_info["phone_number"],
#                                                 full_name=user_info["full_name"], password=user_info["password"])
#                 code.delete()
#                 messages.success(
#                     request, f"{user.full_name} shoma sabt nam kardid", "success")
#                 return redirect("accounts:user_login")
#             except RGScode.DoesNotExist:
#                 messages.error(request, "code eshteba ast", "danger")
#         return render(request, self.template_name, {"form": form})