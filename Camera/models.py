from django.db import models
from utils import file_upload_to
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
    address=models.CharField( verbose_name=_("Address"),max_length=1000, null=True, blank=False)
    ph_no=models.CharField(verbose_name=_("Phone No"),max_length=100,null=True, blank=False)
    name=models.CharField( verbose_name=_("Full Name"),max_length=1000, null=True, blank=False)
    shop_name=models.CharField(verbose_name=_("Shop Name"), max_length=1000, null=True, blank=False)
    username=models.CharField( verbose_name=_("User Name"),max_length=200, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField( max_length=255, null=True , blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location =models.CharField(verbose_name=_("Location"),max_length=1000, null=True, blank=True)
    cnic_no = models.CharField(verbose_name=_("CNIC NO"),max_length=1000, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
    objects = UserManager()


    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['username']
    def __unicode__(self):
            return "%s" % self.username


class Record(models.Model):
    person_selling_name=models.CharField(verbose_name=_("Selling Person Name"), max_length=200, null=False, blank=False)
    person_selling_cnic=models.CharField( verbose_name=_("Selling Person CNIC"),max_length=200, null=False, blank=False)
    person_selling_address=models.CharField(verbose_name=_("Selling Person Address"), max_length=200, null=False, blank=False)
    person_selling_phone=models.CharField(verbose_name=_("Selling Person Ph#"),max_length=200,null=True, blank=False)
    phone_make=models.CharField(verbose_name=_("Equipment Name"), max_length=200, null=False, blank=False)
    phone_model=models.CharField( verbose_name=_("Equipment Model"),max_length=200, null=False, blank=False)
    imei_no=models.CharField(verbose_name=_("IMEI NO"), max_length=200, null=False, blank=False)
    phone_sold_date=models.DateTimeField(verbose_name=_("Phone SO"),default=timezone.now, blank=True,null=True)
    user_id=models.ForeignKey(Client, related_name='record')
    cnic_front = models.ImageField(verbose_name=_("CNIC Front Side"), upload_to=file_upload_to, max_length=2000, null=True, blank=True)
    cnic_back = models.ImageField(verbose_name=_("CNIC Back Side"), upload_to=file_upload_to, max_length=2000, null=True, blank=True)
    signature = models.ImageField(verbose_name=_("Signature"), upload_to=file_upload_to, max_length=2000, null=True, blank=True)
    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Records')
        ordering = ['-phone_sold_date']

    def __unicode__(self):
            return "%s" % self.user_id.username


# Create your models here.
