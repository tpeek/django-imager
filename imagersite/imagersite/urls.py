from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from imagersite.views import home_view


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_view, name='homepage'),
    url(r'^', include('imager_profile.urls')),
    url(r'^', include('imager_images.urls')),
    url(r'^', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
