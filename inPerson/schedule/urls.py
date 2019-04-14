from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('user/', views.ListCreateRecurrentEventsView.as_view(),
        name='get-schedule-add-event'),
    path('<int:pk>/', views.RecurrentEventsDetailView.as_view(),
        name ='create-update-delete-recurrent-event'),



]
