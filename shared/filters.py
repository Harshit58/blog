from rest_framework import filters


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        q = request.GET.get('q', None)

        if q:
            return queryset.filter(content__icontains=q)
        return queryset