from django.urls import include, path

from . import views

urlpatterns = [
    # path('<slug:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    path('<int:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    # path('', views.UserListView.as_view()),

]
