from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

# TODO: NOTE: It would have been much easier to take this approach with a dictionary-driven design
# on selecting the appropriate serializer class based on action: https://stackoverflow.com/a/22922156/1412781
# Maybe something we can consider for the future, it would simplify the need for all these custom
# classes and give the viewsets the most flexibilit yfor CRUD and custom actions.


class BaseCreateModelMixin(mixins.CreateModelMixin):
    """
    This is Base create model mixin which inherits the create model mixin and override the create
    function of DRF to change the serializer for responses. Make sure you have defined
    get_response_serializer_class where you will inherit this base create mixin otherwise it will just
    use the serializer class defined in viewset for the APIs
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)

        # Changing the serializer to read serializer to always send full info
        # in response after create
        serializer = self.get_response_serializer_class()(obj)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Needed to over ride it send back the object to catch it in create
        obj = serializer.save()
        return obj


class BaseListModelMixin(mixins.ListModelMixin):
    """
    This is Base list model mixin which inherits the list model mixin and it will override the list function
    from DRF so that we can change the serializer for responses. Make sure you have defined
    get_response_serializer_class where you will inherit this base list mixin otherwise it will just
    use the serializer class defined in viewset for the APIs
    """
    pass


class BaseRetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    This is Base retrieve model mixin which inherits the retrieve model mixin which get the one
    extra positional argument 'use_user' if use_user is set to true then it will return the object of
    user otherwise it will return the object of model and it will override the retrieve
    function of DRF so that we can change the serializer for response. Make sure you have defined
    get_response_serializer_class where you will inherit this base retrieve mixin otherwise
    it will just use the serializer class defined in viewset for the APIs
    """
    pass


class BaseUpdateModelMixin(mixins.UpdateModelMixin):
    """
    This is Base update model mixin which inherits the update model mixin which get the one
    extra positional argument 'use_user' if use_user is set to true then it will return the object of
    user otherwise it will return the object of model and it will override the update
    function from DRF so that we can change the serializer for responses. Make sure you have defined
    get_response_serializer_class where you will inherit this base update mixin otherwise it will just
    use the serializer class defined in viewset for the APIs
    """
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # Changing the serializer to read serializer to always send full
        # info in response after update
        serializer = self.get_response_serializer_class()(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_response_serializer_class(self):
    #     return self.serializer_class

    # def get_serializer_class(self):
    #     if self.action in [DRFActions.LIST, DRFActions.GET]:
    #         return self.get_response_serializer_class()
    #     return self.serializer_class


class BaseDestroyModelMixin(mixins.DestroyModelMixin):
    """
    This is Base destroy model mixin which inherits the destroy model mixin and it will override the destroy
    function from DRF so that we can change the serializer for responses. Make sure you have defined
    get_response_serializer_class where you will inherit this base destroy mixin otherwise it will just
    use the serializer class defined in viewset for the APIs
    """
    pass