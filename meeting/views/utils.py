from django.views.generic import View
from django.template.loader import render_to_string
from django.http import JsonResponse


class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context


#  AJAX helper
def save_reservation_form(request, form, template_name, additional_context={}):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    context.update(additional_context)
    data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)
