from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from utils import FileUpload

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
        if self.name == '' and self.family == '':
            return self.mobile_number
        else:
            return f"{self.name} {self.family}"

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


# ====================================================================================================
class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='customer_mode')
    phon_number = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    file_upload = FileUpload('images', 'customers')
    image_name = models.ImageField(upload_to=file_upload.upload_to, null=True, blank=True, verbose_name='تصویر پروفایل')

    def __str__(self):
        return f"{self.user}"


    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'


class Message(models.Model):
    full_name = models.CharField(max_length=40, verbose_name='نام')
    email = models.EmailField(max_length=80, verbose_name='ایمیل')
    subject = models.CharField(max_length=100, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    is_seen = models.BooleanField(default=False, verbose_name='وضعیت مشاهده توسط مدیر')
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ ثبت پیام')

    def __str__(self):
        return self.full_name + ' ' + self.subject

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
        db_table = 't_messages'