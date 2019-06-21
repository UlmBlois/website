from django.core import validators
# from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

import logging

from radio_call_sign_field.validators import validate_radio_call_sign
from radio_call_sign_field.widgets import CallSingPrefixWidget

logger = logging.getLogger(__name__)


class CallSignField(CharField):
    default_error_messages = {"invalid":
                              _("str_invalide_aircraft_registration_number")
                              }
    default_validators = [validate_radio_call_sign]
    widget = CallSingPrefixWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        val = super().to_python(value)
        if val in validators.EMPTY_VALUES:
            return self.empty_value
        return val

    def validate(self, value):
        super().validate(value)
        validate_radio_call_sign(value)
