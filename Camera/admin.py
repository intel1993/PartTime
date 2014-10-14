__author__ = 'Abdul Rehman'
from django.contrib import admin
from models import Record,Client
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

# Now register the new UserAdmin...
admin.site.register(Client, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.register(Record)