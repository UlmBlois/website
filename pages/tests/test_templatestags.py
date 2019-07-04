from django.test import TestCase
from django.template import Context
from django.conf import settings
from django.test.client import RequestFactory

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

    @classmethod
    def setUpTestData(cls):
        settings.DEFAULT_DOMAIN = 'http://testserver'
        cls.factory = RequestFactory()

    def test_absolute_url(self):
        context = Context()
        url = absolute_url(context, 'index')
        self.assertEqual(url, settings.DEFAULT_DOMAIN+"/meeting/")
        request = self.factory.get('/meeting/')
        context['request'] = request
        url = absolute_url(context, 'index')
        self.assertEqual(url, settings.DEFAULT_DOMAIN+"/meeting/")
