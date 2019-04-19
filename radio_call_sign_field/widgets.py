from django.forms import Select, TextInput
from django.forms.widgets import MultiWidget
from django_countries.fields import Country


COUTRIES_PREFIX = (
    ('DE', 'D-'),  # Allemagne
    ('AT', 'OE-'),  # Autriche
    ('BE', 'OO-'),  # Belgique
    ('BG', 'LZ-'),  # Bulgarie
    ('CY', '5B-'),  # Chypre
    ('HR', '9A-U'),  # Croatie
    ('DK', 'OY-'),  # Danemark
    ('ES', 'EC-'),  # Espagne
    ('EE', 'ES-'),  # Estonie
    ('FI', 'OH-'),  # Finlande
    ('FR', 'F-J'),  # France
    ('GR', 'SX-'),  # Grece
    ('HU', 'HA-'),  # Hongrie
    ('IE', 'EI-'),  # Irlande
    ('IT', 'I-'),  # Italie
    ('LV', 'YL-'),  # Lettonie
    ('LT', 'LY-'),  # Lituanie
    ('LU', 'LX-X'),  # Luxembourg
    ('MT', '9H-'),  # Malte
    ('NL', 'PH-'),  # Pays Bas
    ('PL', 'SP-'),  # Pologne
    ('PT', 'CR-'),  # Portugal
    ('CZ', 'OK-'),  # Republique Tcheque
    ('RO', 'YR-'),  # Roumanie
    ('GB', 'G-'),  # Royaume Unis
    ('SK', 'OM-'),  # Slovaquie
    ('SI', 'S5-'),  # Slovenie
    ('SE', 'SE-'),  # Suede
    # TODO Fill the list, rethink choice data
)


class CallSignPrefixSelect(Select):
    initial = None

    def __init__(self, initial=None):
        choices = [("", "---------")]
        for country_code, prefix in COUTRIES_PREFIX:
            country = Country(country_code)
            if country:
                choices.append((prefix, "%s %s" % (country.name, prefix)))

        super().__init__(
            choices=sorted(choices, key=lambda item: item[1])
        )


class CallSingPrefixWidget(MultiWidget):

    def __init__(self, attrs=None, initial=None):
        widgets = (
            CallSignPrefixSelect(initial),
            TextInput(attrs=attrs)
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            start = [x[1] for x in COUTRIES_PREFIX
                     if value.startswith(x[1])]
            if len(start) == 0:
                return [None, value]
            id = value.replace(start[0], '')
            return [start[0], id]
        return [None, ""]

    def value_from_datadict(self, data, files, name):
        parts = [widget.value_from_datadict(data, files, name + '_%s' % i)
                 for i, widget in enumerate(self.widgets)]
        return ''.join(parts)
