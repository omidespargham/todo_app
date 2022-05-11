import email
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.views import View
from django.contrib import messages
from accounts.forms import UserLogInForm, UserRegisterForm, UserRegisterVerifyForm
from accounts.models import RGScode
from .models import User


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
            self.request.session["user_info"] = {
                "phone_number": cl["phone_number"],
                "email": cl["email"],
                "full_name": cl["full_name"],
                "password": cl["password"]
            }
            random_code = randint(0, 9999)
            # sms to user
            RGScode.objects.create(
                phone_number=cl["phone_number"], code=random_code)
            return redirect("accounts:user_register_verify")
        return render(request, self.template_name, {"form": form})


class UserRegisterVerifyView(View):
    form_class = UserRegisterVerifyForm
    template_name = "accounts/register.html"

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
            code = form.cleaned_data["code"]
            try:
                user_info = request.session["user_info"]
                code = RGScode.objects.get(
                    phone_number=user_info["phone_number"], code=code)
                user = User.objects.create_user(email=user_info["email"], phone_number=user_info["phone_number"],
                                                full_name=user_info["full_name"], password=user_info["password"])
                code.delete()
                messages.success(
                    request, f"{user.full_name} shoma sabt nam kardid", "success")
                return redirect("accounts:user_login")
            except RGScode.DoesNotExist:
                messages.error(request, "code eshteba ast", "danger")
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

class UserProfileView(LoginRequiredMixin,View):
    template_name = "accounts/user_profile.html"
    def get(self,request):
        return render(request,self.template_name)

