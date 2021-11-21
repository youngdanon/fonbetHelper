from django.urls import path
from . import views


urlpatterns = [
    path('live_events', views.live_events_request, name='live_events')
]
