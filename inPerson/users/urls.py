from django.urls import include, path

from . import views

urlpatterns = [
    # path('<slug:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    path('', views.UserListView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view(), name="users-detail"),
    path('follow/<int:pk>', views.FollowersRelationshipDetailView.as_view(),
         name="send-delete-follow-request"),
    path('following/', views.FollowsListView.as_view(), name="following-list"),
    path('followers/', views.FollowersListView.as_view(), name="followers-list"),
    # path('friendships/', views.FriendsListView.as_view(), name="friends-list")
]
