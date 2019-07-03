from django.shortcuts import reverse
from django import template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, view_name, *args, **kwargs):
    request = context.get('request', None)
    url = ''
    if request is not None:
        url = request.build_absolute_uri(
                reverse(view_name, args=args, kwargs=kwargs))
    else:
        url = "{domain}{reverse}".format(
            domain=settings.DEFAULT_DOMAIN,
            reverse=reverse(view_name, args=args, kwargs=kwargs))
    return url
