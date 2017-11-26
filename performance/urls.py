from django.conf.urls import url
from django.views.generic import TemplateView

from performance import views

urlpatterns = [

    url(r'^performance-dashboard/$', views.performance, name='performance_dashboard')
]
