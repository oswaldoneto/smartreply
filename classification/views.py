import json

from django.views.generic.base import View
from django.http.response import HttpResponse

from classification.models import Classification


class UpdateClassificationView(View):

    def get(self, request, *args, **kwargs):

        with open('/Users/oswaldo/complain.json') as data:
            data = json.load(data)

        problem_list = []
        for complain in data:
            problem_list.append(complain['category'])

        problem_list = set(problem_list)

        for problem in problem_list:
            if not Classification.objects.filter(name=problem).exists():
                Classification.objects.create(name=problem)

        return HttpResponse()
