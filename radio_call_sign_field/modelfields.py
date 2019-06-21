from django.utils.translation import ugettext_lazy as _
from django.db import models

from radio_call_sign_field.validators import validate_radio_call_sign
from radio_call_sign_field import formfields


class RadioCallSignField(models.CharField):
    default_validators = [validate_radio_call_sign]
    description = _("str_Aircraft_registration_number")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": formfields.CallSignField,
            "error_messages": self.error_messages,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
