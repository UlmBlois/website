from django.test import TestCase
# from django.db.utils import IntegrityError

from core.models import User


class CaseInsensitiveUserNameManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1",
                                             password="azerty",
                                             email="user1@test.fr")

    def test_get_by_natural_key(self):
        user = User.objects.get_by_natural_key('user1')
        self.assertEqual(user.username, 'user1')
        user = User.objects.get_by_natural_key('uSEr1')
        self.assertEqual(user.username, 'user1')

    def test_create_user_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username="user1",
                                     password="azerty",
                                     email="user12@test.fr")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="usER1",
                                     password="azerty",
                                     email="user13@test.fr")

    def test_create_user_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username="user2",
                                     password="azerty",
                                     email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="user2",
                                     password="azerty",
                                     email="user1@test.fr")
