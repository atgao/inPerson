from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    # list information
    path('user/following/', login_required(views.FollowsListView.as_view()), name="following-list"),
    path('user/followers/', login_required(views.FollowersListView.as_view()), name="followers-list"),
    path('user/blocks/', login_required(views.BlocksListView.as_view()), name="blocked-users-list"),

    # follower actions actions
    path('follow/<int:pk>/', login_required(views.FollowerRequestsDetailView.as_view()),
         name="send-delete-follow-request"),
    path('unfollow/<int:pk>/', login_required(views.FollowsDestroyView.as_view()), name="unfollow"),
    path('cancel/<int:pk>/', login_required(views.FollowerRequestsCancelView.as_view()),
         name='cancel-follow-request'),
    path('remove/<int:pk>/', login_required(views.FollowersRemoveDetailView.as_view()), name="remove-follower"),

    # requests
    path('user/requests/', login_required(views.FollowerRequestsListView.as_view()),
          name="list-follow-requests"),
    path('user/requests/<int:pk>/', login_required(views.FollowerRequestsCreateView.as_view()),
         name="accept-follow-requests"),

    # blocks
    path('blocks/<int:pk>/', login_required(views.BlocksCreateGetDeleteView.as_view()),
         name="block-check-blocks-unblock")


]
