import sys
import os
import datetime
import dateutil.parser
import httplib2
import json
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.tools import argparser, run_flow
from oauth2client import tools
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone
import pytz, argparse, re

def auth(flags):
  print('auth')
  clientfn = ".credentials/credentials.json"
  try:
    json_data = open("/home/oddcron/{0}".format(clientfn)).read()
    data = json.loads(json_data)
    if 'installed' in data: data = data['installed']
    __API_CLIENT_ID__ = data['client_id']
    __API_CLIENT_SECRET__ = data['client_secret']
  except:
    print('Could not read', clientfn)
    exit() 

  storage = Storage("token.json")
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    flow = OAuth2WebServerFlow(
                      client_id=__API_CLIENT_ID__,
                      client_secret=__API_CLIENT_SECRET__,
                      scope=['https://www.googleapis.com/auth/calendar',
                              'https://www.googleapis.com/auth/urlshortener'],
                      redirect_uri='urn:ietf:wg:oauth:2.0:oob',
                      euser_agent='CalenderInviter')
    flags=tools.argparser.parse_args(args=['--noauth_local_webserver'])
    credentials = run_flow(flow, storage, flags)
    
  # else:
  #   try:
  #     json_data = open('token.json').read()
  #     data = json.loads(json_data)
  #     __API_CLIENT_ID__ = data['client_id']
  #     __API_CLIENT_SECRET__ = data['client_secret']
  #     flow = OAuth2WebServerFlow(
  #                     client_id=__API_CLIENT_ID__,
  #                     client_secret=__API_CLIENT_SECRET__,
  #                     scope=['https://www.googleapis.com/auth/calendar',
  #                             'https://www.googleapis.com/auth/urlshortener'],
  #                     redirect_uri='urn:ietf:wg:oauth:2.0:oob',
  #                     euser_agent='CalenderInviter')
  #     flags=tools.argparser.parse_args(args=['--noauth_local_webserver'])
  #     credentials = run_flow(flow, storage, flags)
  #     authHttp = credentials.authorize(httplib2.Http())
  #   except Exception as e:
  #     print('Could not read token.json %s' % e)
  #     exit() 
  
  
  authHttp = credentials.authorize(httplib2.Http())
  service = build(serviceName='calendar', version='v3', http=authHttp)

  return service

#Returns start time and end time
def create_date_time_gcal():
  '''
  Convert YYYYMMDD formatted string to date object.
  '''
  date = datetime.now(tz=pytz.utc)
  date = date.astimezone(timezone('US/Pacific'))
  one_hour_from_now = date + timedelta(hours=1)
  rounded_start_time = hour_rounder(one_hour_from_now)
  print(str(rounded_start_time)[11:16])
  current_time_hours = str(date)[11:19]
  start_time_of_event = datetime.strptime(str(rounded_start_time)[11:16], "%H:%M")
  # start_time_of_event = d.strftime("%I:%M")


  one_hour_event = datetime.strptime(str(start_time_of_event)[11:16], "%H:%M") + timedelta(hours=1)
  # rounded_end_time = hour_rounder(one_hour_event)
  print('End time' , str(one_hour_event)[11:16])

  end_time_of_event = datetime.strptime(str(one_hour_event)[11:16], "%H:%M")
  # end_time_of_event = d.strftime("%I:%M")

  start_time = datetime.utcnow().strftime('%Y-%m-%dT{0}-{1}'.format(str(start_time_of_event)[11:19],'03:00'))
  end_time = datetime.utcnow().strftime('%Y-%m-%dT{0}-{1}'.format(str(end_time_of_event)[11:19],'03:00'))
  print(start_time, end_time)
  return start_time,end_time

def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               + timedelta(hours=1))

def create_attendees_list(emails):
  email_split = emails.split(',')
  attendees = []
  for email in email_split:
    em = {'email': email}
    attendees.append(em)
  return attendees

def get_description(filename):
  description = ""
  with open(filename, "r+") as f:
    for lines in f:
      description += lines + "\n"  
    
  return description

def verify_correct_date_time_format(date):
  if date is not None:
    date_with_offset = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}")
    date_no_offset = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}")
    correct_date_with_offset_pattern = date_with_offset.match(date)
    correct_date_no_offset_pattern = date_no_offset.match(date)
    if correct_date_with_offset_pattern:
      return correct_date_with_offset_pattern
    elif correct_date_no_offset_pattern:
      return correct_date_no_offset_pattern
  else:
    return False

def main(flags): 
  
  service = auth(flags)
  # print(flags)
  if flags.start_time is None:
    start_time, end_time = create_date_time_gcal()
  else:
    if verify_correct_date_time_format(flags.start_time):
      start_time = flags.start_time
    else: 
      print("Start time is in incorrect format! Please use: 2022-10-05T18:00:00-03:00")
      exit(0)
    if verify_correct_date_time_format(flags.end_time):
      end_time = flags.end_time
    else: 
      print("End time is in incorrect format! Please use: 2022-10-05T18:00:00-03:00")
      exit(0)

  attendees = create_attendees_list(flags.emails)
  print(attendees)
  print("Event starts at {start_time} and ends at {end_time}".format(start_time=start_time, end_time=end_time))

  description = get_description(flags.file)

  event = {
  'summary': flags.summary,
  'location': 'Zoom',
  'description': description,
  'start': {
    'dateTime': '{start_time}'.format(start_time=start_time),
    'timeZone': 'America/New_York',
    #'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '{end_time}'.format(end_time=end_time),
    'timeZone': 'America/New_York',
    #'timeZone': 'America/Los_Angeles',
  },
  'guestsCanSeeOtherGuests': False,
  # 'recurrence': [
  #   'RRULE:FREQ=DAILY;COUNT=1'
  # ],
  'attendees': attendees,
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 10},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Send Gcal Invites to Users")
  # tools.argparser.add_argument_group('standard')
  # group = parser.add_mutually_exclusive_group()
  # group.add_argument("-e", "--emails", action="store_true")
  # group.add_argument("-q", "--quiet", action="store_true")
  parser.add_argument("-e", "--emails", help="Comma seperated list of emails to send invite to", required=True)
  parser.add_argument("-s", "--summary", help="Summary for the meeting", required=True)
  # parser.add_argument("-n", "--noauth_local_webserver", help="Don't auth locally and get code from browser for creds", required=True, action='store_true')
  parser.add_argument("-f", "--file", help="File containing html of event description", required=True)
  parser.add_argument("-st", "--start-time", help="The start time of the meeting, must be in Gcal format of YYYY-MM-DDTHH:MM:SS-HH:MM (e.g: 2022-10-05T15:00:00-03:00)")
  parser.add_argument("-et", "--end-time", help="The end time of the meeting, must be in Gcal format of YYYY-MM-DDTHH:MM:SS-HH:MM (e.g: 2022-10-05T15:00:00-03:00)")
  args = parser.parse_args()
  # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
  # args.noauth_local_webserver = True
  flags, args = parser.parse_known_args()
  # print(flags)
  # print(args.emails)

  main(flags)