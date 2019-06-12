from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(takes_context=True)
def render(context, value):
    return template.Template(value).render(context)
