from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CaseInsensitiveUserNameManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CaseInsensitiveUserNameManager()
