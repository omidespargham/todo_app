from email.policy import default
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11,
                                    unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ("email", "full_name")

    def __str__(self):
        return f"{self.phone_number} - {self.full_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class RGScode(models.Model):
    phone_number = models.CharField(max_length=11,unique=True)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RGS_Code"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    img = models.ImageField(null=True,blank=True,default="default/default.jpg")
    
    def __str__(self):
        return f"{self.user}"