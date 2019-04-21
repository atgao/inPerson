from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:pk>/', views.UserDetailView.as_view(), name="users-detail"),

]
