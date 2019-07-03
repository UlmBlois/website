from django.test import TestCase
from django.template import Context
from pages.models import Chunk, Page
from pages.templatetags.chunks import get_chunk
from pages.templatetags.render import render
from pages.templatetags.absolute_url import absolute_url


class GetChunkTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pg = Page.objects.create(slug='page_1')
        cls.chunk = Chunk.objects.create(page=pg,
                                         key='chunk1')

    def test_get_chunk(self):
        self.assertEqual(get_chunk('chunk1'), self.chunk)
        self.assertIsNone(get_chunk(''))


class RenderTest(TestCase):

    def test_render(self):
        template = "{% if var == True %}1{%else%}2{%endif%}"
        context = Context({
            'var': True
            })
        self.assertEqual(render(context, template), "1")


class AbsoluteUrlTest(TestCase):

    def test_absolute_url(self):
        context = Context()
        url = absolute_url(context, 'index')
        self.assertEqual(url, "http://127.0.0.1:8000/meeting/")
        # TODO
