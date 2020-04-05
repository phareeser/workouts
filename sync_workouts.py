import argparse

#from garminconnect import GarminConnect
#from workout_importer import WorkoutImporter

"""
Command line tool used to sync workouts from Garmin Connect or local files 
with a database or local files.
Duplicate workouts are detected and enriched with missing information

Author: Martin Reese
Project motivation: Introduce myself into Python
"""

import logging

from garmin_importer import GarminImporter

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action='count', help="increase verbosity, from -v (ERROR) over -vv (WARNING), -vvv (INFO) to -vvvv (DEBUG)")
parser.add_argument("source", help="source to import workouts from", choices=['garmin', 'csv', 'json'])
parser.add_argument("-sf", "--sourcefilename", help="source filename")
# parser.add_argument("dest", help="location to store workouts. If existing, sync source with dest", choices=['csv', 'json'])
parser.add_argument("-df", "--destfilename", help="destination filename")
parser.add_argument("-gu", "--garminuser", help="garmin connect user name")
parser.add_argument("-gp", "--garminpwd", help="garmin connect password")
parser.add_argument('--version', action='version', version='%(prog)s 0.01')
args = parser.parse_args()

if not args.verbose or args.verbose > 4:
  log_level = "CRITICAL"
else:
  log_levels = [logging.NOTSET, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
  log_level = log_levels[args.verbose]
logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

if (args.source == 'garmin'):
  importer = GarminImporter(args.garminuser, args.garminpwd)
else:  
  print("Importers others than Garmin are not yet implemented")
  exit

# TODO handle exceptions !!!!!!!!!!!!111

importer.create_session()
importer.import_workouts()
importer.close_session()
