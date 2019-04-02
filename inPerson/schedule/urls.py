from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^classes/<int:pk>/$', views.SectionsDetailView.as_view(), name="section-details"),
    # path('classes/<int:pk>/', views.SectionsDetailView.as_view(), name="section-details"),

    url(r'^classes/', views.ListSectionsView.as_view(), name = 'sections-all'),
    url(r'^events/', views.ListRecurrentEventsView.as_view(), name = 'recurrent-events-all'),
    path('events/<int:pk>/', views.RecurrentEventsDetailView.as_view(), name = 'recurrent-events-get'),
    url(r'^schedules/', views.ListSchedulesView.as_view(), name = 'schedules-all')

]
