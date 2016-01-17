from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^faker/', include('faker.urls')),
    url(r'^admin/', admin.site.urls),
]