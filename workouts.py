"""
Command line tool used to sync workouts from Garmin Connect or local files 
with a database or local files.
Duplicate workouts are detected and enriched with missing information

Author: Martin Reese
Project motivation: Introduce myself to Python
"""

import logging
import argparse
from datetime import date

from lib.garmin_importer import GarminImporter
from lib.json_importer import JsonImporter
from lib.json_exporter import JsonExporter
from lib.csv_importer import CsvImporter
from lib.csv_exporter import CsvExporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action='count',
                    help="increase verbosity, from -v (ERROR) over -vv (WARNING), -vvv (INFO) to -vvvv (DEBUG)")
parser.add_argument("action", help="show workouts, import from external source, export, check for duplicates or create sample files", choices=[
                    'show', 'import', 'export', 'check', 'sample'])
parser.add_argument("database", help="the workouts database")
parser.add_argument("-s", "--source", help="source to import workouts from",
                    choices=['garmin', 'csv', 'json'])
parser.add_argument("-d", "--destination",
                    help="destination format to export workouts to", choices=['csv', 'json'])
parser.add_argument("-f", "--filename",
                    help="filename to import from or export to")
parser.add_argument("-gu", "--garminuser", help="garmin connect user name")
parser.add_argument("-gp", "--garminpwd", help="garmin connect password")
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
args = parser.parse_args()

# logging
if not args.verbose or args.verbose > 4:
    log_level = "CRITICAL"
else:
    log_levels = [logging.NOTSET,
                  logging.ERROR,
                  logging.WARNING,
                  logging.INFO,
                  logging.DEBUG]
    log_level = log_levels[args.verbose]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

if (args.action == "import") and not args.database:
    args.database = "sample.db"

db = WorkoutsDatabase(args.database)
if not db.create_session():
    print("could not access database {}".format(args.database))
    exit

if (args.action == "import"):
    # import from source
    importer = None
    if (args.source == 'garmin'):
        importer = GarminImporter(args.garminuser, args.garminpwd)
    elif (args.source == 'csv'):
        importer = CsvImporter(args.filename)
    elif (args.source == 'json'):
        importer = JsonImporter(args.filename)
    else:
        print("importer {} not implemented".format(args.source))
    if importer:
        if importer.create_session():
            importer.import_workouts(db)
        importer.close_session()
elif (args.action == "export"):
    # export to destination
    exporter = None
    if (args.destination == 'csv'):
        exporter = CsvExporter(args.filename)
    elif (args.destination == 'json'):
        exporter = JsonExporter(args.filename)
    else:
        print("exporter {} not implemented".format(args.destination))
    if exporter:
        if exporter.create_session():
            exporter.export_workouts(db)
        exporter.close_session()
elif (args.action == "show"):
    db.showall()
elif (args.action == "check"):
    db.check()
elif (args.action == "sample"):
    db.create_sample()
    if not args.filename:
        args.filename = "sample"
    csvExporter = CsvExporter(args.filename + ".csv")
    jsonExporter = JsonExporter(args.filename + ".json")
    if csvExporter.create_session():
        csvExporter.export_workouts(db)
        csvExporter.close_session()
    if jsonExporter.create_session():
        jsonExporter.export_workouts(db)
        jsonExporter.close_session()

db.close_session()
