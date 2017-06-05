
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new', views.NewMessageView.as_view(), name='processor-new'),
    url(r'^message/(?P<id>\d+)/classify$', views.ClassifyMessageView.as_view(), name='processor-message-by-id-classify'),
    url(r'^message/(?P<id>\d+)/respond$', views.RespondMessageView.as_view(), name='processor-message-by-id-respond'),
]

