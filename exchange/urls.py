
from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^fetchall$', views.FetchAllView.as_view(), name='exchange-fetchall'),
]

