from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):

  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    now = timezone.now()
    if not username:
      raise ValueError(_('The given username must be set'))
    email = self.normalize_email(email)
    user = self.model(username=username, email=email,
             is_staff=is_staff, is_active=False,
             is_superuser=is_superuser, last_login=now,
             date_joined=now, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email=None, password=None, **extra_fields):
    return self._create_user(username, email, password, False, False,
                 **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True,
                 **extra_fields)
    user.is_active=True
    user.save(using=self._db)
    return user


class Client(AbstractBaseUser, PermissionsMixin):
    address=models.CharField( max_length=1000, null=True, blank=False)
    ph_no=models.CharField(max_length=100,null=True, blank=False)
    name=models.CharField( max_length=1000, null=True, blank=False)
    shop_name=models.CharField( max_length=1000, null=True, blank=False)
    username=models.CharField( max_length=200, null=False, blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField( max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
    objects = UserManager()


class Record(models.Model):
    person_selling_name=models.CharField( max_length=200, null=False, blank=False)
    person_selling_cnic=models.CharField( max_length=200, null=False, blank=False)
    person_selling_address=models.CharField( max_length=200, null=False, blank=False)
    person_selling_phone=models.CharField(max_length=200,null=True, blank=False)
    phone_make=models.CharField( max_length=200, null=False, blank=False)
    phone_model=models.CharField( max_length=200, null=False, blank=False)
    imei_no=models.CharField( max_length=200, null=False, blank=False)
    phone_sold_date=models.DateTimeField(default=timezone.now, blank=True,null=True)
    user_id=models.ForeignKey(Client, related_name='record')
from django.db import models

# Create your models here.
