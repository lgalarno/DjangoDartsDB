from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import StaticViewSitemap

app_name = 'dartsDBweb'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name="main"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), ),
    path('about/', TemplateView.as_view(template_name="index.html"), name="about"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('login/', LoginView.as_view(), name = "login"),
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('PlayersManagement/', include('PlayersManagement.urls', namespace ="PlayersManagement")),
    path('score/', include('gamescoring.urls', namespace ="gamescoring")),
    path('table/', include('scoretable.urls', namespace ="scoretable")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
