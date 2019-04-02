from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^classes/<int:pk>/$', views.SectionsDetailView.as_view(), name="section-details"),
    # path('classes/<int:pk>/', views.SectionsDetailView.as_view(), name="section-details"),

    url(r'^classes/search/$', views.ListSectionsView.as_view(), name = 'search-sections'),
    url(r'^events/', views.ListRecurrentEventsView.as_view(), name = 'recurrent-events-all'),
    url(r'^schedules/', views.ListSchedulesView.as_view(), name = 'schedules-all')

]
