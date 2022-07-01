from datetime import datetime
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view

from googleapiclient.discovery import build

from .utils import client





@api_view(['GET'])
def AuthView(request):
    response = client()
    response.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'
    authorization_url, state = response.authorization_url(include_granted_scopes='true',access_type='offline')
    request.session['state'] = state
    return redirect(authorization_url)



@api_view(['GET'])
def CalendarView(request):
    state = request.session.get('state')    
    response = client(state)
    response.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'
    authorization_response = request.get_full_path()
    response.fetch_token(authorization_response=authorization_response)
    credentials = response.credentials

    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.utcnow().isoformat() + 'Z'
        all_events_result = service.events().list(calendarId='primary').execute()
        all_events = all_events_result.get('items', [])
        upcoming_events_result = service.events().list(calendarId='primary',timeMin=now,singleEvents=True,orderBy='startTime').execute()
        upcoming_events = upcoming_events_result.get('items', [])

        if not all_events:
            return Response({'Message': 'No events found.'})
        else:

            all_events_list = []
            for event in all_events:
                event_dict = {
                    'event_id': event['id'],
                    'name': event['summary'],
                    'creator': event['creator'],
                    'organizer': event['organizer'],
                    'start_time': event['start'],
                    'end_time': event['end']
                }
                all_events_list.append(event_dict)
            upcoming_events_list = []
            for event in upcoming_events:
                event_dict = {
                    'event_id': event['id'],
                    'name': event['summary'],
                    'creator': event['creator'],
                    'organizer': event['organizer'],
                    'start_time': event['start'],
                    'end_time': event['end']
                }
                upcoming_events_list.append(event_dict)
            final_list= [{'Upcoming Events ':upcoming_events_list, 'All Events ':all_events_list}]
            return Response(final_list)

    except Exception as error:
        return Response({'Message': 'Found an Error : %s' % error})


