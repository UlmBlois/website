from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import re

# TODO size can vary between state, make full verification

RADIO_CALL_SIGN_REGEX = r'^[0-9a-zA-Z]{1,2}-[0-9a-zA-Z]{3,4}$'


def validate_radio_call_sign(value):
    size = len(value)
    if size != 6:
        raise ValidationError(
            _("Invalid value: %(size)s charaters, expected 6 charaters."),
            code='invalid', params={'size': size})
    if re.fullmatch(RADIO_CALL_SIGN_REGEX, value) is None:
        raise ValidationError(
            _("Invalid value: does not match the format XX-YYY or X-YYYY"),
            code='invalid')
