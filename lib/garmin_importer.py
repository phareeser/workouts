"""
Class for importing workouts from Garmin Connect
"""

import requests
import re
import json
import logging

from lib.workout_importer import WorkoutImporter

GARMIN_SSO_URL       = "https://sso.garmin.com"
GARMIN_SSO_LOGIN_URL = "https://sso.garmin.com/sso/signin"
GARMIN_SERVICE_URL   = "https://connect.garmin.com/modern"
GARMIN_SESSION_URL   = "https://connect.garmin.com/legacy/session"


GARMIN_ACTIVITIES_SEARCH = "https://connect.garmin.com/modern/proxy/activitylist-service/activities/search/activities"
GARMIN_GPX_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/%d?full=true&#8220;"
GARMIN_KML_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.0/kml/activity/%d?full=true&#8220;"
GARMIN_TCX_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.0/tcx/activity/%d?full=true&#8220;"


class GarminImporter(WorkoutImporter):

  def _authenticate(self):
    logging.info("signing in to Garmin ...")
    
    form_data = {
      "username": self.username,
      "password": self.password,
      "embed": "false"
    }
    params = {"service": GARMIN_SERVICE_URL}
    headers={'origin': GARMIN_SSO_URL}
    response = self.session.post(GARMIN_SSO_LOGIN_URL, headers=headers, params=params, data=form_data)

    #logging.debug("RESPONSE HEADERS: {}".format(response.headers))
    #logging.debug("RESPONSE TEXT: {}".format(response.text))
    if response.status_code != 200:
      raise ValueError("sign in failed")
    title = re.search(r'<title>(.*?)</title>', response.text)
    if title:
      logging.info("Garmin responded with {}".format(title.group(1)))
    else:
      logging.warning("NO TITLE FOUND IN RESPONE")
        
    # response contains 'response_url', looking like this:
    # response_url = "https:\/\/connect.garmin.com\/modern?ticket=ST-05295530-W4lJ5jIeFPz5MgPgHvND-cas";
    # we need to GET the response_url in order to finalize the authentication process
    match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', response.text)
    if not match:
      raise RuntimeError("authentication failed")
    authentication_url = match.group(1).replace("\\", "")
    response = self.session.get(authentication_url)
    #logging.debug("RESPONSE HEADERS: {}".format(response.headers))
    #logging.debug("RESPONSE TEXT: {}".format(response.text))

    if response.status_code != 200:
      raise RuntimeError(
        "authentication failed: {}: {}\n{}".format(authentication_url, response.status_code, response.text))

    title = re.search(r'<title>(.*?)</title>', response.text)
    if title:
      logging.info("logged in to {}".format(title.group(1)))
    else:
      logging.warning("NO TITLE FOUND IN RESPONE")

  def __init__(self, username, password):
    logging.info("garmin importer initializing ...")
    self.username = username
    self.password = password
    self.session = None

  def create_session(self):
    logging.info("garmin importer creating session ...")
    self.session = requests.Session()
    self._authenticate()
  
  def close_session(self):
    logging.info("garmin importer closing session ...")
    if self.session:
      self.session.close()
      self.session = None
    logging.info("session closed")
  
  def import_workouts(self, db):
    logging.info("fetching workouts ...")
    params = {
      "start": 0,
      "limit": 200 }
    response = self.session.get(GARMIN_ACTIVITIES_SEARCH, params=params)
    if response.status_code != 200:
      raise ValueError("error reading workouts")
    workouts = response.json()
    with open("workouts.json", "w") as file:
      json.dump(workouts, file)
    file.close()
  
