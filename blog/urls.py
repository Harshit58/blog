from django.urls import path, include

from blog.views import BlogAPIViewSet, CommentAPIViewSet, LikeCreateAPIView, LikeDeleteAPIView
from shared.utils import NoPutRouter


router = NoPutRouter()


urlpatterns = [
    path('like', LikeCreateAPIView.as_view(), name='create-like'),
    path('like/<int:pk>/', LikeDeleteAPIView.as_view(), name='delete-like'),
]

router.register('comment', CommentAPIViewSet, base_name='Comment')

router.register('', BlogAPIViewSet, base_name='Blog')


urlpatterns += [
    path('', include(router.urls)),
]