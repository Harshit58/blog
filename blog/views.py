from rest_framework import mixins, viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from django.shortcuts import render

from blog.models import Blog, Comment, Like
from blog.serializers import (
    BlogSerializer, BlogReadSerializer, UserProfileSerializer, ChangePasswordSerializer, CommentSerializer,
    CommentReadSerializer, LikeSerializer
)

from shared.views import BaseAPIViewSet
from shared.filters import UserFilterBackend


class BlogAPIViewSet(BaseAPIViewSet):
    '''
    '''

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = (UserFilterBackend, )

    def get_response_serializer_class(self):
        return BlogReadSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.get_response_serializer_class()
        return self.serializer_class


class MyProfileAPIView(RetrieveUpdateAPIView):
    '''
    '''

    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(request.user, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the request.user.
            request.user._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(CreateAPIView):
    '''
    '''

    serializer_class = ChangePasswordSerializer


class CommentAPIViewSet(BaseAPIViewSet):
    '''
    '''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_response_serializer_class(self):
        return CommentReadSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.get_response_serializer_class()
        return self.serializer_class


class LikeCreateAPIView(CreateAPIView):
    '''
    '''

    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        blog_id = request.data.get('blog')

        if Like.objects.filter(user=request.user, blog__id=blog_id).exists():
            Like.objects.filter(user=request.user, blog__id=blog_id).delete()
        else:
            super().create(request, *args, **kwargs)

        blog = Blog.objects.get(id=blog_id)

        return Response(BlogReadSerializer(blog).data, status=status.HTTP_201_CREATED)


class LikeDeleteAPIView(DestroyAPIView):
    '''
    '''

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response({'message': "You have successfully deleted the like."}, status=status.HTTP_204_NO_CONTENT)
