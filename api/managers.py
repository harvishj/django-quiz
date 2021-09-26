from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import override, ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, alias=None, **extra_fields):
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, alias=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user.save()
        return user

    # def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     return super().__call__(*args, **kwds)