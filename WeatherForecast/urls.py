from django.conf.urls import url, include

urlpatterns = [
    url(r'^async/', include('async.urls')),
    url(r'^cities/', include('cities.urls')),
    url(r'^forecast/', include('forecast.urls')),
]
