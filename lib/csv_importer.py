# coding=utf-8

from lib.workout_importer import WorkoutImporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase
import logging
import csv
from datetime import datetime

logger = logging.getLogger(__name__)


class CsvImporter(WorkoutImporter):
    """
    Imports workouts from CSV file to database
    """
    def __init__(self, filename):
        logger.info("csv importer initializing ...")
        self.csv = None
        self.filename = filename

    def create_session(self):
        logger.info("csv importer creating session ...")
        try:
            self.csv = open(self.filename, "r")
        except FileNotFoundError:
            logger.error("csv input file not found")
            return False
        except TypeError:
            logger.error("import filename not correct")
            return False
        return True

    def close_session(self):
        logger.info("csv importer closing session ...")
        if self.csv:
            self.csv.close()
        self.csv = None

    def import_workouts(self, db):
        """
        Imports workouts into a database
        from a list of csv records 
        """
        logger.info("fetching workouts ...")
        total_fetched_workouts = 0
        total_imported_workouts = 0

        keys = Workout.header()
        workouts = csv.DictReader(self.csv)
        # TODO check if header is correct


        ################################################################
        counter = 0

        if self.csv:
            for record in workouts:
                counter += 1
                if counter > 3:
                    break
                logger.debug('CSV record: {}'.format(record))
                workout = Workout()
                total_fetched_workouts += 1
                for key in keys:
                    if key == "start_time":
                        record[key] = datetime.strptime(record[key], "%Y-%m-%d %H:%M:%S")
                    elif key == "id":
                        workout.external_id = record[key]
                        continue
                    elif key == "sportstype":
                        sportstype = SportsType(name = record[key])
                        if record["name"]:
                            workout.name = record["name"]     # necessary for sportstype association
                        sportstype.add(workout, db)
                        workout.sportstype_id = sportstype.id
                        workout.sport_id = sportstype.sport_id
                        continue
                    setattr(workout, key, record[key])
                    if getattr(workout, key) == '':
                        setattr(workout, key, None)
                if 'source' not in keys or record['source'] == '' or record['source'] == None:
                    workout.source = "CSV import"
                logger.debug('WORKOUT: {}'.format(workout))
                if workout.add(db):
                    total_imported_workouts += 1

        logger.info("{} workouts fetched and {} workouts imported".format(
            total_fetched_workouts, total_imported_workouts))
        
        return(total_fetched_workouts, total_imported_workouts)
