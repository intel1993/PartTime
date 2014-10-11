import xadmin
from models import Record,Client
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# xadmin.site.unregister(Client)
# Register your models here.
# class MyUserAdmin(UserAdmin):
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2')}
#         ),
#     )
# from django.contrib.auth.models import User
# xadmin.site.unregister(Client)
# xadmin.site.register(Client, MyUserAdmin)
xadmin.site.register(Record)