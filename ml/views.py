import json

from django.http.response import HttpResponse
from django.views.generic.base import View, TemplateView
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


class StatusView(TemplateView):
    template_name = 'status.html'



