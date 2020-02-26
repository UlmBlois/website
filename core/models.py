from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from django.db import models


class CaseInsensitiveUserNameManager(UserManager):

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, username, email, password=None, **extra_fields):
        if len(self.filter(username__iexact=username)) > 0:
            raise ValueError(_('str_Username_already_used'))

        if not email:
            raise ValueError(_('str_Email_required'))
        email = self.normalize_email(email)

        if len(self.filter(email__exact=email)) > 0:
            raise ValueError(_('str_Email_already_used'))

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CaseInsensitiveUserNameManager()
