from django.urls import path
from .views import (
    GoogleOAuth2InitView,
    GoogleOAuth2CallbackView,
)

urlpatterns = [
    path("init/", GoogleOAuth2InitView.as_view(), name="google_oauth2_init"),
    path(
        "callback/",
        GoogleOAuth2CallbackView.as_view(),
        name="google_oauth2_callback",
    ),
    # path('google/calendar/events/', GoogleOAuth2EventsView.as_view(), name='google_calendar_events'),
]
