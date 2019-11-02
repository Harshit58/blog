from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from blog.views import MyPrfileAPIView, ChangePasswordAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Blog API', permission_classes=[]), name='Documentation'),
    path('login', obtain_jwt_token, name='login'),
    path('my-profile', MyPrfileAPIView.as_view(), name='my-profile'),
    path('change-password', ChangePasswordAPIView.as_view(), name='change-password')
]

urlpatterns += [
    path('blogs/', include('blog.urls'))
]