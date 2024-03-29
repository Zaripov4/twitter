from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Twitter API",
        default_version="v1",
        description="Twitter clone",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token", TokenObtainPairView.as_view(), name="TokenObtainView"),
    path("api/refresh/token", TokenRefreshView.as_view(), name="TokenRefreshView"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
    path("docs2/", schema_view.with_ui("redoc", cache_timeout=0), name="docs2"),
    path("", include("blog.urls")),
]
