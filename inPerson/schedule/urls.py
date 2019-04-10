from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('user/', views.ListRecurrentEventsView.as_view(),
        name='schedule-recurrevents-list-create-individual'),
    path('events/<int:pk>/', views.RecurrentEventsDetailView.as_view(),
        name ='recurrent-events-get'),

    # classes urls
    path('schedule/classes/', views.CreateSectionstoScheduleView.as_view(),
        name='add-class-to-schedule')

]
