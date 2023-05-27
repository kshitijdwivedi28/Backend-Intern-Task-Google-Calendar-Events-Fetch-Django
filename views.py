from django.http import HttpResponse, JsonResponse
from django.views import View
from google.auth import exceptions
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www/googleapis.com/auth/calendar.readonly']
CLIENT_SECRET_FILE = 'path/to/client_secret.json'
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'


class GoogleCalendarInitView(View):

  def get(self, request):
    # Getting credentials and authorization
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE,
                                                     SCOPES)

    authorization_url, state = flow.authorization_url(
      access_type='offline', include_granted_scopes='true')

    # Preserving state for CSRF token
    request.session['google_auth_state'] = state

    return JsonResponse({'authorization_url': authorization_url})


class GoogleCalendarRedirectView(View):

  def get(self, request):
    # Handle redirect request sent by google with code for token
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Verifying the earlier stored state
    if state != request.session.get('google_auth_state'):
      return HttpResponse('Invalid state', status=400)

    # Getting Access token by sending Authorization
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE,
                                                     SCOPES)
    try:
      flow.fetch_token(code=code, redirect_uri=REDIRECT_URI)
    except exceptions.OAuth2Error as e:
      return HttpResponse(str(e), status=400)

    credentials = flow.credentials

    # Getting list of events (max. 10) from user's calendar
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary',
                                          maxResults=10).execute()
    events = events_result.get('items', [])

    # Building result i.e., list of events
    event_list = []
    for event in events:
      event_list.append(event['summary'])

    return JsonResponse({'events': event_list})
