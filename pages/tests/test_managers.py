from django.test import TestCase
from pages.models import Chunk


class ChunkManagerTest(TestCase):

    @classmethod
    def setUpTestData(self):
            Chunk.objects.create(key="chunk1")

    def test_safe_get(self):
        ch = Chunk.objects.safe_get(key="chunk1")
        self.assertIsNotNone(ch)
        ch = Chunk.objects.safe_get(key="chunk")
        self.assertIsNone(ch)
