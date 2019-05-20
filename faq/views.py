from django.views.generic.list import ListView
from faq.models import Topic


# Create your views here.
class FAQView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'faq.html'
