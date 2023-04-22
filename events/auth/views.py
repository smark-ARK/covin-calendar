from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime


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
        try:
            service = build("calendar", "v3", credentials=credentials)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
        except HttpError as error:
            print("An error occurred: %s" % error)

        request.session["google_oauth2_credentials"] = credentials.to_json()

        return Response({"events": events})


# class GoogleOAuth2EventsView(APIView):
#     def get(self, request):
#         credentials = Credentials.from_authorized_user_info(info=request.session.get('google_oauth2_credentials'))
#         events = # Call the Google Calendar API to get the user's events
#         return Response(events)
