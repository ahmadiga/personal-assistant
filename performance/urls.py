from django.conf.urls import url
from django.views.generic import TemplateView

from performance import views

urlpatterns = [

    url(r'^performance-dashboard/$', views.performance, name='performance_dashboard'),
    url(r'^list-team/$', views.team_performance, name='list_team'),
    url(r'^team-performance-dashboard/(\d+)$', views.team_performance_dashboard, name='team_performance_dashboard'),

]
