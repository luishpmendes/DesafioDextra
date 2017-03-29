from django.conf.urls import url

from . import views

app_name = 'startupAlimentos'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^lanche/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^lanche/(?P<lanche_id>[0-9]+)/pedir/$', views.pedir, name='pedir'),
    url(r'^lanche/$', views.montarLanche, name='montarLanche'),
]
