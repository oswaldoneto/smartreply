
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^status', views.StatusView.as_view(), name='ml-status'),
    url(r'^predict$', views.predict_view),
    url(r'^evaluate$', views.evaluate_view),
    url(r'^loaddata$', views.load_data),
    url(r'^loadtarget$', views.load_targets),
]

