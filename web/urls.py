from django.conf.urls import patterns, url
from Wifiledlamps.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
