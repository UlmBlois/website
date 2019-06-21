from django.forms import Select
from django.utils.translation import gettext_lazy as _


# TODO raise ValidationError if Unknown is Select
class BooleanWidget(Select):
    """Convert true/false values into the internal Python True/False.
    This can be used for AJAX queries that pass true/false from JavaScript's
    internal types through.
    """

    def __init__(self, attrs=None):
        choices = (('', _('str_Unknown')),
                   ('true', _('str_Yes')),
                   ('false', _('str_No')))
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = {
                True: 'true',
                False: 'false',
                '1': 'true',
                '0': 'false'
            }[value]
        except KeyError:
            value = ''
        return super().render(name, value, attrs, renderer=renderer)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if isinstance(value, str):
            value = value.lower()

        return {
            '1': True,
            '0': False,
            'true': True,
            'false': False,
            True: True,
            False: False,
            }.get(value, None)
