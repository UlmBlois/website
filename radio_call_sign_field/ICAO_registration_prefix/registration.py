import re
import logging

from .data import PATTERNS_DICT

logger = logging.getLogger(__name__)


class RegistrationNumber:
    def __init__(self, number=''):
        logger.debug('create RegistrationNumber')
        self.number = number
        if len(number) > 0:
            self.validator = Validator.fromNumber(number)

    def is_valid(self):
        return self.validator.validate(self.number)


class Validator:
    def __init__(self, prefix='', patterns=[]):
        self.prefix = prefix
        self.patterns = patterns

    @classmethod
    def fromNumber(cls, number):
        logger.debug('create RegistrationNumber Validator')
        pattern_list = []
        key_max_size = 0
        key_best_match = ''
        for key, patterns in PATTERNS_DICT.items():
            if number.startswith(key):
                pattern_list.append(key)
                if key_max_size < len(key):
                    key_max_size = len(key)
                    key_best_match = key
        return cls(key_best_match, PATTERNS_DICT[key_best_match])

    def validate(self, number):
        for p in self.patterns:
            if re.match(self.prefix+p, number):
                return True
        return False
