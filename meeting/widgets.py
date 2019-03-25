from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

COUTRIES_PREFIX = (
    ('D-', 'D-'),  # Allemagne
    ('OE-', 'OE-'),  # Autriche
    ('OO-', 'OO-'),  # Belgique
    ('LZ-', 'LZ-'),  # Bulgarie
    ('5B-', '5B-'),  # Chypre
    ('9A-U', '9A-U'),  # Croatie
    ('OY-', 'OY-'),  # Danemark
    ('EC-', 'EC-'),  # Espagne
    ('ES-', 'ES-'),  # Estonie
    ('OH-', 'OH-'),  # Finlande
    ('F-J', 'F-J'),  # France
    ('SX-', 'SX-'),  # Grece
    ('HA-', 'HA-'),  # Hongrie
    ('EI-', 'EI-'),  # Irlande
    ('I-', 'I-'),  # Italie
    ('YL-', 'YL-'),  # Lettonie
    ('LY-', 'LY-'),  # Lituanie
    ('LX-X', 'LX-X'),  # Luxembourg
    ('9H-', '9H-'),  # Malte
    ('PH-', 'PH-'),  # Pays Bas
    ('SP-', 'SP-'),  # Pologne
    ('CR-', 'CR-'),  # Portugal
    ('OK-', 'OK-'),  # Republique Tcheque
    ('YR-', 'YR-'),  # Roumanie
    ('G-', 'G-'),  # Royaume Unis
    ('OM-', 'OM-'),  # Slovaquie
    ('S5-', 'S5-'),  # Slovenie
    ('SE-', 'SE-'),  # Suede
    # TODO Fill the list, rethink choice data
)


class ULMRadioIdWidget(widgets.MultiWidget):
        template_name = 'widgets/ulm_radio_id_widget.html'

        def __init__(self, attrs=None):
            _widgets = (
                widgets.Select(attrs=attrs, choices=COUTRIES_PREFIX),
                widgets.TextInput(attrs=attrs)
            )
            super().__init__(_widgets, attrs)

        def value_from_datadict(self, data, files, name):
            parts = [widget.value_from_datadict(data, files, name + '_%s' % i)
                     for i, widget in enumerate(self.widgets)]
            return ''.join(parts)

        def decompress(self, value):
            if value:
                prefix = [x[0] for x in COUTRIES_PREFIX]
                start = [x for x in prefix if value.startswith(x)][0]
                id = value.replace(start, '')
                return [start, id]
            return [None, None]
