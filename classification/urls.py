
from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^update', views.UpdateClassificationView.as_view(), name='classification-update'),
]

