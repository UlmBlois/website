from django import template
from django.template import Context, Template
from pages.models import Chunk

register = template.Library()


@register.simple_tag
def get_chunk(key):
    return Chunk.objects.get(key=key)


class RenderCustom(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.split_contents()

        field = tokens[1]

        return cls(parser.compile_filter(field))

    def __init__(self, field):
        self.field = field

    def render(self, context):
        render_field = self.field.resolve(context)

        render_template = Template(render_field)

        rendered = render_template.render(Context())

        return rendered


@register.tag
def evaluate(parser, token):
    return RenderCustom.handle_token(parser, token)
