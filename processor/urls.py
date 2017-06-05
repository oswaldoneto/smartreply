
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new', views.NewMessageView.as_view(), name='processor-new'),
    url(r'^message/(?P<id>\d+)/classify$', views.ClassifyMessageView.as_view(), name='processor-message-by-id-classify'),
    url(r'^respond', views.NewRespondMessageView.as_view(), name='processor-new'),
    url(r'^message/(?P<id>\d+)/respond$', views.RespondMessageView.as_view(), name='processor-message-by-id-respond'),

    url(r'^callback/(?P<id>\d+)/mba$', views.MBAView.as_view(), name='processor-message-by-id-mba'),
    url(r'^callback/(?P<id>\d+)/cobit$', views.CobitView.as_view(), name='processor-message-by-id-cobit'),
    url(r'^callback/(?P<id>\d+)/scrum$', views.ScrumView.as_view(), name='processor-message-by-id-scrum'),

]

