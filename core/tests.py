from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse, path
from django.conf import settings
from django.contrib.messages import constants as messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseServerError, HttpResponseBadRequest
from core import views

from meeting.tests.utils import ViewTestCase, LoggedViewTestCase, create_user
from salon_ulm_blois.urls import urlpatterns as main_patterns


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


def permission_denied_view(request):
    raise PermissionDenied


def not_found_view(request):
    raise Http404


def server_error_view(request):
    return HttpResponseServerError()


def bad_request_view(request):
    return HttpResponseBadRequest()


urlpatterns = main_patterns + [
    path('403/', permission_denied_view, name='403'),
    path('404/', not_found_view, name='404'),
    path('400/', bad_request_view, name='400'),
    path('500/', server_error_view, name='500'),
]

handler403 = views.handler_403
handler404 = views.handler_404
handler400 = views.handler_400
handler500 = views.handler_500

# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF=__name__, DEBUG=False)
class CustomErrorHandlerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user("user", "testtest")

    def test_handler_403(self):
        response = self.client.get(reverse('403'))
        # Make assertions on the response here. For example:
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_handler_403_logged(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('403'))
        # Make assertions on the response here. For example:
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'logged_403.html')

    def test_handler_404(self):
        response = self.client.get(reverse('404'))
        # Make assertions on the response here. For example:
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_handler_404_logged(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('404'))
        # Make assertions on the response here. For example:
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'logged_404.html')

    # @override_settings(DEBUG=False)
    # def test_handler_400(self):
    #     response = self.client.get(reverse('400'))
    #     # Make assertions on the response here. For example:
    #     self.assertEqual(response.status_code, 400)
    #     self.assertTemplateUsed(response, '400.html')
    #
    # @override_settings(DEBUG=False)
    # def test_handler_400_logged(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse('400'))
    #     # Make assertions on the response here. For example:
    #     self.assertEqual(response.status_code, 400)
    #     self.assertTemplateUsed(response, 'logged_400.html')
    #
    # @override_settings(DEBUG=False)
    # def test_handler_500(self):
    #     response = self.client.get(reverse('500'))
    #     # Make assertions on the response here. For example:
    #     self.assertEqual(response.status_code, 500)
    #     self.assertTemplateUsed(response, '500.html')
    #
    # @override_settings(DEBUG=False)
    # def test_handler_500_logged(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse('500'))
    #     # Make assertions on the response here. For example:
    #     self.assertEqual(response.status_code, 500)
    #     self.assertTemplateUsed(response, 'logged_500.html')
