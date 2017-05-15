
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^run$', views.RunView.as_view(), name='processor-run'),
]

