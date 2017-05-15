
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new', views.NewMessageView.as_view(), name='processor-new'),
    url(r'^message/(?P<id>\d+)$', views.MessageView.as_view(), name='processor-message-by-id'),
]

