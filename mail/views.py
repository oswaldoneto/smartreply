from django.shortcuts import render
from django.views.generic.base import TemplateView

from mail.models import Message


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({'new_messages': Message.objects.filter(state=1)})
        context.update({'classified_messages': Message.objects.filter(state=3)})
        context.update({'answered_messages': Message.objects.filter(state=4)})
        context.update({'failure_messages': Message.objects.filter(state=5)})
        return context

