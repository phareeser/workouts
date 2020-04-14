"""
Command line tool used to sync workouts from Garmin Connect or local files 
with a database or local files.
Duplicate workouts are detected and enriched with missing information

Author: Martin Reese
Project motivation: Introduce myself into Python
"""

import logging
import argparse

from garmin_importer import GarminImporter
from workoutsdb import WorkoutsDB

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action='count', help="increase verbosity, from -v (ERROR) over -vv (WARNING), -vvv (INFO) to -vvvv (DEBUG)")
parser.add_argument("action", help="show workouts, import from external source or check for duplicates", choices=['show', 'import', 'check'])
parser.add_argument("database", help="the workouts database")
parser.add_argument("-s", "--source", help="source to import workouts from", choices=['garmin', 'csv', 'json'])
parser.add_argument("-f", "--filename", help="source filename")
parser.add_argument("-gu", "--garminuser", help="garmin connect user name")
parser.add_argument("-gp", "--garminpwd", help="garmin connect password")
parser.add_argument('--version', action='version', version='%(prog)s 0.01')
args = parser.parse_args()

# logging
if not args.verbose or args.verbose > 4:
  log_level = "CRITICAL"
else:
  log_levels = [logging.NOTSET, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
  log_level = log_levels[args.verbose]
logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

# database
workoutsDB = WorkoutsDB(args.database)
workouts = []
workouts.append({'id': 2, 'source': 'garmin', 'name': 'laufen', 'date': '2020-04-02sfsdfsd'})
workouts.append({'id': 3, 'source': 'csv', 'name': 'radfahren', 'date': '2020-04-03'})
workoutsDB.insert_workouts(workouts)
workoutsDB.close()

if (args.action == "show"):
  pass
elif (args.action == "import"):
  # import from source
  if (args.source == 'garmin'):
    importer = GarminImporter(args.garminuser, args.garminpwd)
  elif (args.source == 'csv'):  
    print("csv importer not yet implemented")
    exit
  elif (args.source == 'json'):  
    print("json importer not yet implemented")
    exit
  else:
    print("importer {} not implemented".format(args.source))
    exit

  # TODO handle exceptions !!!!!!!!!!!!

  importer.create_session()
  importer.import_workouts()
  importer.close_session()
elif (args.action == "check"):
  pass