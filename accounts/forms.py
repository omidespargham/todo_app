from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import RGScode, User
from django.core.validators import MaxLengthValidator, MinLengthValidator


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(
        validators=[MaxLengthValidator(11), MinLengthValidator(11)])
    email = forms.EmailField()
    full_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        # try:
        user = User.objects.filter(phone_number=phone)
        rgs = RGScode.objects.filter(phone_number=phone)
        if user:
            raise forms.ValidationError("karbar ba in phone voojood darad !")
        if rgs:
            rgs.delete()
        return phone
        # except User.DoesNotExist:
            

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("karbar ba in email voojood darad !")
        except User.DoesNotExist:
            return email

class UserRegisterVerifyForm(forms.Form):
    code = forms.IntegerField()

class UserLogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# there are for User Model implementatioon

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        help_text="change password from <a href=\" ../password/\">this form</a>")

    class Meta:
        model = User
        fields = ["email", "phone_number",
                  "full_name", "password", "last_login"]

# User profile Edit

class UserProfileEditForm(forms.ModelForm):
    img = forms.ImageField()
    class Meta:
        model = User
        fields= ["email","phone_number","full_name"]
        
