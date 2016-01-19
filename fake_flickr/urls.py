from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^faker/', include('faker.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/faker/')),   
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)