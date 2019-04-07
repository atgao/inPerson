from django.urls import include, path

from . import views

urlpatterns = [
    path('follow/<int:pk>/', views.FollowerRequestsDetailView.as_view(),
         name="send-delete-follow-request"),
    path('user/following/', views.FollowsListView.as_view(), name="following-list"),
    path('user/followers/', views.FollowersListView.as_view(), name="followers-list"),
    path('unfollow/<int:pk>/', views.FollowsDestroyView.as_view(), name="unfollow"),
    path('remove/<int:pk>/', views.FollowersRemoveDetailView.as_view(), name="remove-follower"),
    path('user/requests/<int:pk>/', views.FollowerRequestsListView.as_view(),
         name="list-accept-follow-requests"), # unsure if the GET method works
    path('follow/<int:pk>/', views.FollowerRequestsDetailView.as_view(),
         name="create-delete-follow-request"),
    path('cancel/<int:pk>/', views.FollowerRequestsCancelView.as_view(),
         name='cancel-follow-request')
    # path('friendships/', views.FriendsListView.as_view(), name="friends-list")
]
