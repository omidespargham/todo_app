from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib import admin
from .models import Profile, RGScode, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class RGScodeAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")


admin.site.register(RGScode, RGScodeAdmin)


class MyUserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin', "is_active")
    list_filter = ("is_admin",)
    search_fields = ("full_name", "email")

    fieldsets = (
        (None, {"fields": ("email", "phone_number", "full_name", "password")}),
        ("permissions", {"fields": ("is_active", "is_admin", "last_login")})
    )

    add_fieldsets = (
        (None, {"fields": ("email", "phone_number",
         "full_name", "password")}),
    )
    filter_horizontal = ()
    ordering = ("full_name",)
    inlines = (MyUserProfileInline,)


admin.site.unregister(Group)

admin.site.register(User, MyUserAdmin)

