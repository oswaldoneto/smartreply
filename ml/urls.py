
from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^status', views.StatusView.as_view(), name='ml-status'),
]

