# Backend-Intern-Task-Google-Calendar-Events-Fetch-Django

## Problem: 
In this assignment you have to implement google calendar integration using django rest api. You need to use the OAuth2 mechanism to get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement -
/rest/v1/calendar/init/ -> GoogleCalendarInitView() - This view should start step 1 of the OAuth. Which will prompt user for his/her credentials
/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView() - This view will do two things
1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar

You need to write the code in Django. You are not supposed to use any
existing third-party library other then google’s provided standard libraries

## Solution - 

The result code is written in views.py presuming the app is built and this feature is to be added. Also, the urls for the API are mentioned in urls.py file in order to map the endpoints.
Approach -
1. In GoogleCalendarInitView(), 3 variables are chosen considering google calendar integration -
i) SCOPES => Used as an access point to the calendar for integration.
ii) CLIENT_SECRET_FILE => Path to client JSON file from Google
iii) REDIRECT_URI => To get the authorization code from Google

Now created a OAuth2 flow object, and thereby generated authorization url, which is returned as a JSON response to the client, initiating to get credentials.
Also the state is stored to be verified later on considering the CSRF token.

2. In GoogleCalendarRedirectView(), code and state parameters are fetched to be verified, and when the user submits the credentials, we get the response on REDIRECT_URI.
Then we create another OAuth2 flow object and fetch the token by sending the authorization through the code we got earlier.
After which, we get credentials. So, now we simply initialize the Google Calendar Service and make API calls to get the user's calendar events, from where we fetch the list of events.

Also, the api endpoints are added in the urls.py

And thus, our task is done!
