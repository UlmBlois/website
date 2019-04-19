from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


class CallSignField(CharField):
    default_error_messages = ["invalid", _("Enter a valid radio call sign.")]
    default_validators = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO a completer

    def to_python(self, value):
        return value # TODO: a completer

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
