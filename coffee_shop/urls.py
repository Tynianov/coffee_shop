"""coffee_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


def trigger_error(request):
    division_by_zero = 1 / 0


schema_view = get_schema_view(
   openapi.Info(
      title="Coffee shop API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('^sentry-debug/', trigger_error),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path('^api/v1/', include('api.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^register-notify-token/',
         FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    re_path(r'^', include('django.contrib.auth.urls')),
]

urlpatterns += i18n_patterns(
    re_path(r'^jet/', include('jet.urls', 'jet')),
    re_path(f"{settings.ADMIN_URL}/", admin.site.urls, name="admin"),
    prefix_default_language=True,
)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
