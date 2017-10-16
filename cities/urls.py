from django.conf.urls import url

from cities import views

urlpatterns = [
    url(r'^download/', views.DownloadView.as_view(), name='download_cities'),
    url(r'^search/', views.SearchView.as_view(), name='search_cities'),
]
