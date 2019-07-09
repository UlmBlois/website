from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib.messages import constants as messages

from meeting.tests.utils import ViewTestCase, LoggedViewTestCase


class SignUpViewTest(ViewTestCase, TestCase):
    url = '/core/singup'
    url_name = 'signup'
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('logged_index')

    def test_form_valid(self):
        form_data = {
            'username': 'toto',
            'first_name': 'toto',
            'last_name': 'toto',
            'email': 'toto@toto.fr',
            'password1': 'tatatata',
            'password2': 'tatatata',
        }
        response = self.client.post(self.get_url(), form_data)
        self.assertRedirects(response, self.get_success_url())
        self.assertTrue(
            User.objects.filter(username=form_data['username']).exists())


class DeleteUserTest(LoggedViewTestCase, TestCase):
    url = '/core/accounts/{}/delete'
    url_name = 'delete_user'
    template_name = 'logged_delete_form.html'

    def get_url(self):
        return self.url.format(self.user.pilot.pk)

    def get_url_from_name(self, args=None, kwargs=None):
        kwargs = {'pk': self.user.pilot.pk}
        return super().get_url_from_name(kwargs=kwargs)

    def get_success_url(self):
        return reverse('index')

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cancel_url'],
                         reverse('pilot', kwargs={'pk': self.user.pk}))

    def test_delete_messages_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, settings.MESSAGE_TAGS[messages.SUCCESS])

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
