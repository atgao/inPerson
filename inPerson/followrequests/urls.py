from django.urls import include, path

from . import views

urlpatterns = [

    # list information
    path('user/following/', views.FollowsListView.as_view(), name="following-list"),
    path('user/followers/', views.FollowersListView.as_view(), name="followers-list"),
    path('user/blocks/', views.BlocksListView.as_view(), name="blocked-users-list"),

    # follower actions actions
    path('follow/<int:pk>/', views.FollowerRequestsDetailView.as_view(),
         name="send-delete-follow-request"),
    path('unfollow/<int:pk>/', views.FollowsDestroyView.as_view(), name="unfollow"),
    path('cancel/<int:pk>/', views.FollowerRequestsCancelView.as_view(),
         name='cancel-follow-request'),
    path('remove/<int:pk>/', views.FollowersRemoveDetailView.as_view(), name="remove-follower"),

    # requests
    path('user/requests/<int:pk>/', views.FollowerRequestsListCreateView.as_view(),
         name="accept-follow-requests"),
    path('user/requests/', views.FollowerRequestsListCreateView.as_view(),
         name="list-follow-requests"),

    # blocks 
    path('blocks/<int:pk>/', views.BlocksCreateGetDeleteView.as_view(),
         name="block-check-blocks-unblock")


]
