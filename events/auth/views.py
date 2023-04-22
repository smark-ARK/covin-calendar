from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response


class GoogleOAuth2InitView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=["openid", "https://www.googleapis.com/auth/calendar.events"],
            redirect_uri=request.build_absolute_uri(reverse("google_oauth2_callback")),
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        request.session["google_oauth2_state"] = state
        return HttpResponseRedirect(authorization_url)


class GoogleOAuth2CallbackView(APIView):
    def get(self, request):
        state = request.session.pop("google_oauth2_state", None)
        flow = Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=["openid", "https://www.googleapis.com/auth/calendar.events"],
            redirect_uri=request.build_absolute_uri(reverse("google_oauth2_callback")),
        )
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        request.session["google_oauth2_credentials"] = credentials.to_json()
        return HttpResponseRedirect("/")


# class GoogleOAuth2EventsView(APIView):
#     def get(self, request):
#         credentials = Credentials.from_authorized_user_info(info=request.session.get('google_oauth2_credentials'))
#         events = # Call the Google Calendar API to get the user's events
#         return Response(events)
