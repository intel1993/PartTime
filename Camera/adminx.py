__author__ = 'Abdul Rehman'
import xadmin
from models import Record,Client,Exceptions
from xadmin.plugins.inline import Inline
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from forms import RegistrationForm,UserChangeForm,UserForm

class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = RegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    generic_inline=True

    list_filter = ('email',)
    exclude = ('password1','password2',)
    fieldsets = (
        (None, {'fields': ('email', 'password','cnic_no',)}),
        ('Personal info', {'fields': ('first_name','last_name',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','address','ph_no','shop_name','username','password','cnic_no','latt_val', 'long_val',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

xadmin.site.unregister(Client)
xadmin.site.register(Record)
xadmin.site.register(Client)
xadmin.site.register(Exceptions)