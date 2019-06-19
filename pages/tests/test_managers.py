from django.test import TestCase
from pages.models import Chunk, Page


class ChunkManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        page1 = Page.objects.create(slug="page1")
        Chunk.objects.create(key="chunk1", page=page1)

    def test_safe_get(self):
        ch = Chunk.objects.safe_get(key="chunk1")
        self.assertIsNotNone(ch)
        ch = Chunk.objects.safe_get(key="chunk")
        self.assertIsNone(ch)
