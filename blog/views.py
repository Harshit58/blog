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


class BlogAPIViewSet(BaseAPIViewSet):
    '''
    '''

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_response_serializer_class(self):
        return BlogReadSerializer

    def get_serializer_class(self):
        if self.action in ['get', 'retrieve']:
            return self.get_response_serializer_class()
        return self.serializer_class


class MyPrfileAPIView(RetrieveUpdateAPIView):
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
        if self.action in ['get', 'retrieve']:
            return self.get_response_serializer_class()
        return self.serializer_class


class LikeCreateAPIView(CreateAPIView):
    '''
    '''

    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

        return Response({'message': "You have successfully liked the blog."}, status=status.HTTP_201_CREATED)


class LikeDeleteAPIView(DestroyAPIView):
    '''
    '''

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response({'message': "You have successfully deleted the like."}, status=status.HTTP_204_NO_CONTENT)
