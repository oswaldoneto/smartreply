import json

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from ml import shortcuts


class StatusView(TemplateView):
    template_name = 'status.html'


def predict_view(request):
    data = {'classification': shortcuts.predict(request.GET['text'])[0]}
    return HttpResponse(json.dumps(data), content_type='application/json')


def evaluate_view(request):
    data = {'accuracy': shortcuts.evaluate_accuracy()}
    return HttpResponse(json.dumps(data), content_type='application/json')


def load_data(request):
    train_data_rows, train_data_size, test_data_rows, test_data_size = shortcuts.load_data_sets()
    data = {
        'train_data_rows': train_data_rows,
        'train_data_size': train_data_size,
        'test_data_rows': test_data_rows,
        'test_data_size': test_data_size
    }
    return HttpResponse(json.dumps(data), content_type='application/json')



def load_targets(request):
    data = {
        'targets': list(set(shortcuts.load_targets()))
    }
    return HttpResponse(json.dumps(data), content_type='application/json')






