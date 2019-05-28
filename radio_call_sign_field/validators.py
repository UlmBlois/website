from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import logging

from .ICAO_registration_prefix.registration import RegistrationNumber

logger = logging.getLogger(__name__)


def validate_radio_call_sign(value):
    reg_num = RegistrationNumber(value)
    if not reg_num.is_valid():
        logger.debug("invalid value : %s does not match %s", reg_num.number, str(reg_num.validator.patterns))
        raise ValidationError(
            _("Invalid value: does not match the format of the registration country"),
            code='invalid')
    else:
        logger.debug("valid RegistrationNumber")
