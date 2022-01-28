from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOld

from .models import User
from api.models import UserTest


class TestInline(admin.StackedInline):
    model = UserTest
    extra = 0


class UserAdmin(UserAdminOld):
    inlines = [
        TestInline,
    ]


admin.site.register(User, UserAdmin)
