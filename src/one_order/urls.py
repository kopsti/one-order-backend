from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

from rest_framework.authentication import SessionAuthentication
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAdminUser
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

API_TITLE = 'One Tool API Documentation'
API_DESCRIPTION = 'This page provides all necessary info for our API.'

urlpatterns = [
    path('one-login/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, public=False,
                                        authentication_classes=[SessionAuthentication, ],
                                        permission_classes=[IsAdminUser, ])),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
    path('', include('one_order.config.rest.urls'))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^(?P<path>.*)', TemplateView.as_view(template_name='angular_index.html'), name='home'),
]
