from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('user/', login_required(views.ListCreateRecurrentEventsView.as_view()),
        name='get-schedule-add-event'),
    path('<int:pk>/', login_required(views.RecurrentEventsDetailView.as_view()),
        name ='create-update-delete-recurrent-event'),



]
