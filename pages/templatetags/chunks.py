from django import template
from pages.models import Chunk

register = template.Library()


@register.simple_tag
def get_chunk(key):
    chunk = Chunk.objects.safe_get(key=key)
    if (chunk and not chunk.display):
        chunk = None
    return chunk
