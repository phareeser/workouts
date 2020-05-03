"""
Command line tool used to sync workouts from Garmin Connect or local files 
with a database or local files.
Duplicate workouts are detected and enriched with missing information

Author: Martin Reese
Project motivation: Introduce myself into Python
"""

import logging
import argparse
from datetime import date

from lib.garmin_importer import GarminImporter
from lib.json_importer import JsonImporter
from lib.json_exporter import JsonExporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action='count', help="increase verbosity, from -v (ERROR) over -vv (WARNING), -vvv (INFO) to -vvvv (DEBUG)")
parser.add_argument("action", help="show workouts, import from external source, export or check for duplicates", choices=['show', 'import', 'export', 'check'])
parser.add_argument("database", help="the workouts database")
parser.add_argument("-s", "--source", help="source to import workouts from", choices=['garmin', 'csv', 'json'])
parser.add_argument("-d", "--destination", help="destination format to export workouts to", choices=['csv', 'json'])
parser.add_argument("-f", "--filename", help="filename to import from or export to")
parser.add_argument("-gu", "--garminuser", help="garmin connect user name")
parser.add_argument("-gp", "--garminpwd", help="garmin connect password")
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
args = parser.parse_args()

# logging
if not args.verbose or args.verbose > 4:
  log_level = "CRITICAL"
else:
  log_levels = [logging.NOTSET, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
  log_level = log_levels[args.verbose]
logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

db = WorkoutsDatabase(args.database)

if (args.action == "import"):
  # import from source
  if (args.source == 'garmin'):
    importer = GarminImporter(args.garminuser, args.garminpwd)
  elif (args.source == 'csv'):  
    print("csv importer not yet implemented")
    exit
  elif (args.source == 'json'):  
    importer = JsonImporter(args.filename)
  else:
    print("importer {} not implemented".format(args.source))
    exit
  importer.create_session()
  importer.import_workouts(db)
  importer.close_session()
  # TODO handle exceptions !!!!!!!!!!!!
elif (args.action == "export"):
  if (args.destination == 'csv'):  
    print("csv exporter not yet implemented")
    exit
  elif (args.destination == 'json'):  
    exporter = JsonExporter(args.filename)
  else:
    print("exporter {} not implemented".format(args.destination))
    exit
  exporter.create_session()
  exporter.export_workouts(db)
  exporter.close_session()
if (args.action == "show"):
  db.showall()
elif (args.action == "check"):
  # TODO
  pass

db.close()
