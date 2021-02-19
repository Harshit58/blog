from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from blog.views import MyProfileAPIView, ChangePasswordAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Blog API', permission_classes=[]), name='Documentation'),
    path('login', obtain_jwt_token, name='login'),
    path('my-profile', MyProfileAPIView.as_view(), name='my-profile'),
    path('change-password', ChangePasswordAPIView.as_view(), name='change-password')
]

aa

urlpatterns += [
    path('blogs/', include('blog.urls'))
]

from django.urls import path
from django.views.generic import TemplateView

urlpatterns += [
    path('index/', TemplateView.as_view(template_name="index.html")),
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
    path('change-password/', TemplateView.as_view(template_name="change_password.html"), name='change-password'),
    path('me/', TemplateView.as_view(template_name="my_profile.html"), name='my-profile'),
    path('add-blog/', TemplateView.as_view(template_name="add_blog.html"), name='add-blog'),
]