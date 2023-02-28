from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email="", name="", family="", active_code=None, password=None, gender=None):
        if not mobile_number:
            raise ValueError("شماره موبایل را وارد کنید!")

        user = self.model(
                    mobile_number=mobile_number,
                    email=self.normalize_email(email),
                    name=name,
                    family=family,
                    active_code=active_code,
                    gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email, name, family, password=None, active_code=None, gender=None):
        user = self.create_user(
                                mobile_number=mobile_number,
                                email=email,
                                name=name,
                                family=family,
                                active_code=active_code,
                                gender=gender,
                                password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ============================================================================================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=200, blank=True)
    name = models.CharField(max_length=150, blank=True)
    family = models.CharField(max_length=150, blank=True)
    GENDER_CHOICES = (('True', 'مرد'), ('False', 'زن'))
    gender = models.CharField(max_length=20, blank=True, choices=GENDER_CHOICES, null=True, default='True')
    register_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    active_code = models.CharField(max_length=50, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email', 'name', 'family']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name}  {self.family}"

    @property
    def is_staff(self):
        return self.is_admin
