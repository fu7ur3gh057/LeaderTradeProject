from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, phone_number: str, password=None) -> Any:
        # if password is None:
        #     raise TypeError("Users should have a password")
        # user = self.model(email=self.normalize_email(email))
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone_number: str, password=None, is_legal=False) -> Any:
        user = self._create_user(phone_number=phone_number, password=password)
        user.save()
        return user

    def create_staff(self, phone_number, password) -> Any:
        user = self._create_user(phone_number, password)
        user.is_staff = True
        user.save()
        return user

    def create_admin(self, phone_number, password) -> Any:
        user = self._create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user
