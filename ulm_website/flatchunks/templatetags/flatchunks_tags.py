from django import template
from flatchunks import models

register = template.Library()


@register.simple_tag
def get_flatchunk(identifier):
    return models.Flatchunks.objects.get(identifier=identifier)
