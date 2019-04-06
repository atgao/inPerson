from django.urls import include, path

from . import views

urlpatterns = [
    # path('<slug:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    path('', views.UserListView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    path('following/', views.FollowsListView.as_view(), name="following-list"),
    path('friendships/', views.FriendsListView.as_view(), name="friends-list")
]
