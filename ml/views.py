import json

from django.http.response import HttpResponse
from django.views.generic.base import View, TemplateView
from ml.shortcuts import predict


class StatusView(TemplateView):
    template_name = 'status.html'


def predict_view(request):
    data = {'classification': predict(request.GET['text'])[0]}
    return HttpResponse(json.dumps(data), content_type='application/json')