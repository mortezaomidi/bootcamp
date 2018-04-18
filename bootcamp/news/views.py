import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView

from bootcamp.news.models import News
from bootcamp.mixins import ajax_required, AuthorRequiredMixin


class NewsListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""
    model = News
    paginate_by = 15


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""
    model = News
    success_url = reverse_lazy("news:list")


@login_required
@ajax_required
def post(request):
    """A function view to implement the post functionality with AJAX."""
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0 and len(post) <= 280:
        posted = News.objects.create(
            user=user,
            content=post,
        )
        html = render_to_string(
            'news/partial_news.html',
            {
                'news': posted,
                'csrf_token': csrf_token,
                'request': request
            })
        return HttpResponse(html)

    else:
        lenght = len(post) - 280
        return HttpResponseBadRequest(
            content=_(f'Text is {lenght} characters longer than accepted.'))
