from django.conf.urls import url
from django.contrib.auth.decorators import  login_required

from . import views

app_name = 'ToppsWebinar'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landing/$', login_required(views.landing), name='landing'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^Quiz1/(?P<question_id>[0-9]+)/$', login_required(views.quiz1_controller), name='quiz1_question'),
    url(r'^(?P<question_id>[0-9]+)/answer/$', views.quiz1_answer, name='answer'),
    url(r'^webinar/$', login_required(views.webinar), name='webinar'),
]