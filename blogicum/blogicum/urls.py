"""URL configuration for blogicum project."""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from blog import views as blog_views

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", include("blog.urls", namespace="blog")
    ),
    # Шаблоны используют `{% url 'registration' %}` без namespace.
    path("auth/registration/", blog_views.registration, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "pages/",
        include("pages.urls", namespace="pages"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
