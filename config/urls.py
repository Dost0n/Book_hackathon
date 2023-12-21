from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from config.views import index

schema_view = get_schema_view(
    openapi.Info(
        title = "Book API",
        default_version = "v1",
        description = "Najon ta'lim",
        terms_of_services = "Book"
    ),
    public = True,
    permission_classes = [permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('book.urls')),


    #swagger

    path('swagger/', schema_view.with_ui(
        "swagger", cache_timeout = 0), name="swagger-swagger-ui"),
    path('redoc/', schema_view.with_ui(
        "redoc", cache_timeout = 0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)