from django.conf.urls import url
from django.contrib.auth.decorators import  login_required

from . import views

app_name = 'ToppsWebinar'
urlpatterns = [
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]