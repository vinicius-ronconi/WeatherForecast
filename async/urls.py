from django.conf.urls import url

from async import views

urlpatterns = [
    url(r'^status', views.AsyncResultView.as_view(), name='async_status'),
]
