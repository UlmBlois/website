from django.core import validators
# from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

from radio_call_sign_field.validators import validate_radio_call_sign
from radio_call_sign_field.widgets import CallSingPrefixWidget


# TODO: does not display validation errors
class CallSignField(CharField):
    default_error_messages = {"invalid": _("Enter a valid radio call sign.")}
    default_validators = [validate_radio_call_sign]
    widget = CallSingPrefixWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        val = super().to_python(value)
        if val in validators.EMPTY_VALUES:
            return self.empty_value
        return val
