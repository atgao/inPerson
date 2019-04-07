from rest_framework import serializers
from .models import User
from friendship.models import Friend, Follow, Block

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'class_year')
        read_only_fields = ('username',)

# # incorporate serializers for friendships
# class FriendsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friend
#         # fields = ('to_user', 'from_user', 'created')
#         fields = '__all__'

class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('followee', 'follower', 'created')
