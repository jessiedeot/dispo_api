from rest_framework.decorators import api_view
from rest_framework import generics
from app.models import Post, User, Profile
from app.serializers import PostSerializer, UserSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Q
from django.core import serializers


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def top_users_list(request):
    users = User.objects.annotate(posts_count=Count('posts')).filter(posts_count__gte=1).order_by('-posts_count')
    serialized_users = serializers.serialize("json", users, fields=('username', 'posts_count'))
    return Response(serialized_users)


@api_view(["POST"])
def follow(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def feed(request, pk):
    following = Profile.objects.filter(user=pk)
    posts = Post.objects.filter(Q(user=pk) | Q(user__in=following.values_list('id', flat=True))).order_by('-timestamp')
    serialized_posts = serializers.serialize("json", posts)
    return Response(serialized_posts)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostList(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
