"""accounts.admin
model registration for accounts application
"""

from api.models import UserTest
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOld

from .models import User


class TestInline(admin.StackedInline):
    """
    Inline model for UserTest
    used in UserAdmin
    """
    model = UserTest
    extra = 0


class UserAdmin(UserAdminOld):
    """
    Custom UserAdmin
    Inherited from the built-in UserAdmin
    just added the TestInline for tests the users has done.
    """
    inlines = [
        TestInline,
    ]


admin.site.register(User, UserAdmin)
