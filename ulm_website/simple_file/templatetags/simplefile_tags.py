from django import template
from simple_file import models

register = template.Library()


@register.simple_tag
def get_simplefile(key):
    return models.SimpleFile.objects.get(key=key)
