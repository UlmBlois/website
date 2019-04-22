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

# class PhoneNumberField(CharField):
#     default_error_messages = {"invalid": _("Enter a valid phone number.")}
#     default_validators = [validate_international_phonenumber]
#
#     def __init__(self, *args, **kwargs):
#         self.region = kwargs.pop("region", None)
#         validate_region(self.region)
#         super(PhoneNumberField, self).__init__(*args, **kwargs)
#         self.widget.input_type = "tel"
#
#     def to_python(self, value):
#         phone_number = to_python(value, region=self.region)
#
#         if phone_number in validators.EMPTY_VALUES:
#             return self.empty_value
#
#         if phone_number and not phone_number.is_valid():
#             raise ValidationError(self.error_messages["invalid"])
#
# return phone_number
