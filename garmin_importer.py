"""
Class for importing workouts from Garmin Connect
"""

import requests
import re

from workout_importer import WorkoutImporter

GARMIN_SSO_URL       = "https://sso.garmin.com"
GARMIN_SSO_LOGIN_URL = "https://sso.garmin.com/sso/signin"
GARMIN_SERVICE_URL   = "https://connect.garmin.com/modern"
GARMIN_SESSION_URL   = "https://connect.garmin.com/legacy/session"

'''
SIGNIN_ATTRIBUTES = {
  service: "https://connect.garmin.com/modern/",
  webhost: 'https://connect.garmin.com/modern',
  source: 'https://connect.garmin.com/signin',
  clientId: 'GarminConnect',
  gauthHost: 'https://sso.garmin.com/sso',
  consumeServiceTicket: 'false',
  redirectAfterAccountLoginUrl: 'https://connect.garmin.com/modern',
  redirectAfterAccountCreationUrl: 'https:77connect.garmin.com/modern',
  locale: 'de',
  id: 'gauth-widget',
  generateExtraServiceTicket: 'true'
}
'''

ACTIVITIES_SEARCH = "https://connect.garmin.com/modern/proxy/activitylist-service/activities/search/activities?start=%d&limit=%d"
GPX_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/%d?full=true&#8220;"
KML_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.0/kml/activity/%d?full=true&#8220;"
TCX_EXPORT = "http://connect.garmin.com/proxy/activity-service-1.0/tcx/activity/%d?full=true&#8220;"


class GarminImporter(WorkoutImporter):

  def _authenticate(self):
    self.log.info("signing in to Garmin ...")
    
    form_data = {
      "username": self.username,
      "password": self.password,
      "embed": "false"
    }
    params = {"service": GARMIN_SERVICE_URL}
    headers={'origin': GARMIN_SSO_URL}
    response = self.session.post(GARMIN_SSO_LOGIN_URL, headers=headers, params=params, data=form_data)

    self.log.debug("POST {}".format(response.url))  
    #self.log.debug("RESPONSE HEADERS: {}".format(response.headers))
    #self.log.debug("RESPONSE TEXT: {}".format(response.text))
    title = re.match(r'<title>', response.text)
    self.log.debug("PAGE TITLE: {}".format(title.group(0)))
        
    if response.status_code != 200:
      raise ValueError("sign in failed")

    # response contains 'response_url', looking like this:
    # response_url = "https:\/\/connect.garmin.com\/modern?ticket=ST-05295530-W4lJ5jIeFPz5MgPgHvND-cas";
    # we need to get the service ticket to finalize authentication
    match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', response.text)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    self.log.debug("REGEX: {}".format(match.group(0)))

    if not match:
      raise RuntimeError("Could not authenticate - login credentials correct?")
    authentication_url = match.group(1).replace("\\", "")
    self.log.debug("AUTHENTICATION URL: {}".format(authentication_url))

    response = self.session.get(authentication_url)
    self.log.debug("GET {}".format(response.url))  
    #self.log.debug("RESPONSE HEADERS: {}".format(response.headers))
    #self.log.debug("RESPONSE TEXT: {}".format(response.text))
    #self.log.debug("PAGE TITLE: {}".format(response.content.title))

    if response.status_code != 200:
      raise RuntimeError(
        "Problem getting authentication ticket from garmin: {}: {}\n{}".format(authentication_url, response.status_code, response.text))

    # ????????????????????????????????????????????????????????????????ß
    self.session.get(GARMIN_SESSION_URL)

  def __init__(self, log_level, username, password):
    super().__init__(log_level)
    self.log.info("garmin importer initializing ...")
    self.username = username
    self.password = password
    self.session = None

  def create_session(self):
    self.log.info("garmin importer creating session ...")
    self.session = requests.Session()
    self._authenticate()
  
  def close_session(self):
    self.log.info("garmin importer closing session ...")
    if self.session:
      self.session.close()
      self.session = None
    self.log.info("session closed")
  
  def import_workouts(self):
    pass
  
