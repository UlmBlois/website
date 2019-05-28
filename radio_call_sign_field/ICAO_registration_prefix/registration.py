import re
import logging

from .data import PATTERNS_DICT

logger = logging.getLogger(__name__)


class RegistrationNumber:
    def __init__(self, number=''):
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

    @staticmethod
    def pattern_to_str(pattern):
        alpha = '[A-Za-z]'
        num = '[0-9]'
        alpha_count = ord('a')
        num_count = 1
        has_alpha = True
        has_num = True
        pattern = pattern.replace('$', '')
        while has_num or has_alpha:
            if has_alpha:
                tmp_str = pattern.replace(alpha, chr(alpha_count), 1)
                if tmp_str == pattern:
                    has_alpha = False
                else:
                    alpha_count += 1
                    pattern = tmp_str
            if has_num:
                tmp_str = pattern.replace(num, str(num_count), 1)
                if tmp_str == pattern:
                    has_num = False
                else:
                    num_count += 1
                    pattern = tmp_str
        return pattern

    def __str__(self):
        str = [self.pattern_to_str(self.prefix + x)for x in self.patterns]
        return ','.join(str)
