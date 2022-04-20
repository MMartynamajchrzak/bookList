from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import environ


env = environ.Env()

urlpatterns = [
    path('books/', include('books.urls')),
    path(f'{env.str("ADMIN_URL")}/', admin.site.urls),
    path("docs/schema/", SpectacularAPIView.as_view(), name="docs"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="docs"), name="swagger-ui"),
]
