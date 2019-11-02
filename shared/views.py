from rest_framework import viewsets

from django.shortcuts import render

from shared import mixins as blog_mixins


class BaseAPIViewSet(
        blog_mixins.BaseListModelMixin,
        blog_mixins.BaseCreateModelMixin,
        blog_mixins.BaseRetrieveModelMixin,
        blog_mixins.BaseUpdateModelMixin,
        blog_mixins.BaseDestroyModelMixin,
        viewsets.GenericViewSet):
    '''
    '''

    def get_response_serializer_class(self):
        return self.serializer_class

