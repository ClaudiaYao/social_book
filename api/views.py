from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer, PostSerializer, LikePostSerializer, FollowerCountSerializer
from core.models import Profile, Post, LikePost, FollowersCount
import uuid

@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/profiles"},
        {"GET": "/api/profile/id"},
        {"GET": "/api/posts"},
        {"GET": "/api/post/id"},
        {"POST": "/api/like_post/id"},
        {"DELETE": "/api/remove_post/id"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]

    return Response(routes)

@api_view(["GET"])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likePost(request, pk):
    post_to_edit = Post.objects.get(id=pk)
    user = request.user
    data = request.data['like']

    likepost = LikePost.objects.filter(owner=user, post=post_to_edit).first()
    
    if likepost is None:
        if data == 1:
            new_likepost = LikePost.objects.create(owner=user, post=post_to_edit)
            new_likepost.save()

            post_to_edit.no_of_likes += 1
            post_to_edit.save()
            return Response("post was liked.")
        else:
            return Response("post was unliked already.")
    else:
        if data == 0:
            likepost.delete()
            post_to_edit.no_of_likes -= 1
            post_to_edit.save()
            return Response("post was unliked.")
        else:
            return Response("post was liked already.")

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removePost(request, pk):

    post_to_delete = Post.objects.get(id = pk)
    Post.objects.delete(post_to_delete)
    return Response("Post was deleted.")