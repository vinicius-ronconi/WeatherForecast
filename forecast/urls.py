from django.conf.urls import url

from forecast import views

urlpatterns = [
    url(r'^search/', views.ForecastView.as_view(), name='search_forecast'),
]
