from rest_framework import serializers
from core.models import Profile, Post, LikePost, FollowersCount


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = Post
        fields = '__all__'

class LikePostSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    post = PostSerializer(many=False)
    class Meta:
        model = LikePost
        fields = '__all__'


class FollowerCountSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer(many=False)
    user = ProfileSerializer(many=False)
    class Meta:
        model = FollowersCount
        fields = '__all__'