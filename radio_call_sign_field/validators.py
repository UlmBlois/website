from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import logging

from aircraft_registration.registration import RegistrationNumber

logger = logging.getLogger(__name__)


def validate_radio_call_sign(value):
    reg_num = RegistrationNumber(value)
    if not reg_num.is_valid():
        logger.debug("invalid value : %s does not match %s",
                     reg_num.number, str(reg_num.validator))
        raise ValidationError(
            _("{val} does not match one of the folowing format : {patterns}"
              ).format(val=reg_num.number, patterns=str(reg_num.validator)),
            code='invalid')
    else:
        logger.debug("valid RegistrationNumber")
