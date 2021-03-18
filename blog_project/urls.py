from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="Blog API description",
      terms_of_service="https://terms_of_service/",
      contact=openapi.Contact(email="contact@mail.su"),
      license=openapi.License(name="Add some license here"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns.extend([
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^redoc-old/$', schema_view.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),

    url(r'^cached/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='cschema-json'),
    url(r'^cached/swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    url(r'^cached/redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
    ]
)
