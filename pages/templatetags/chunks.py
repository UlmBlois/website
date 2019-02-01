from django import template
from pages.models import Chunk

register = template.Library()


@register.simple_tag
def get_chunk(key):
    return Chunk.objects.get(key=key)
