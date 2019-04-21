"""inPerson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from django.views.generic.base import TemplateView
from schedule.views import ListSectionsView, CreateSectionstoScheduleView, ListOtherUserScheduleView, CreateScheduleView
from .views import menu_view

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', menu_view, name="home"),
    path('api/', include('followrequests.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('uniauth.urls.cas_only')),
    path('api/events/', include('schedule.urls')),
    path('api/user/', include('users.urls')),

    # search classes
    # classes urls
    path('api/user/schedule/classes/', CreateSectionstoScheduleView.as_view(),
        name='add-class-to-schedule'),
    path('api/classes/', ListSectionsView.as_view(), name='search-sections'),
    path('api/schedule/<int:pk>/', ListOtherUserScheduleView.as_view(),
         name='get-friends-schedule'),
    path('api/schedule/user', CreateScheduleView.as_view(),
         name='create-schedule')

]
