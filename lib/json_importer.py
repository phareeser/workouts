# coding=utf-8

from lib.workout_importer import WorkoutImporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class JsonImporter(WorkoutImporter):
    """
    Imports workouts in JSON format into a database
    """
    def __init__(self, filename):
        logger.info("json importer initializing ...")
        self.json = None
        self.filename = filename

    def create_session(self):
        logger.info("json importer creating session ...")
        try:
            self.json = open(self.filename, "r")
        except FileNotFoundError:
            logger.error("json input file not found")
            return False
        except TypeError:
            logger.error("import filename not correct")
            return False
        return True


    def close_session(self):
        logger.info("json importer closing session ...")
        if self.json:
            self.json.close()
        self.json = None

    def import_workouts(self, db):
        """
        Imports workouts into a database
        from a list of json records 
        """
        logger.info("fetching workouts ...")
        total_fetched_workouts = 0
        total_imported_workouts = 0

        if (self.json):
            for data in self.json:
                try:
                    records = json.loads(data)
                except json.JSONDecodeError as e:
                    logger.error("JSON file not formatted correctly: {}".format(e.args))
                    break
                for record in records:
                    workout = Workout()
                    total_fetched_workouts += 1
                    for key in record:
                        if key == "start_time":
                            record[key] = datetime.strptime(
                                record[key], "%Y-%m-%d %H:%M:%S")
                        elif key == "id":
                            workout.external_id = record[key]
                            continue
                        elif key == "sportstype":
                            sportstype = SportsType(name=record[key])
                            if record["name"]:
                                # necessary for sportstype association
                                workout.name = record["name"]
                            sportstype.add(workout, db)
                            workout.sportstype_id = sportstype.id
                            workout.sport_id = sportstype.sport_id
                            continue
                        setattr(workout, key, record[key])
                    if 'source' not in record:
                        workout.source = "JSON import"
                    if workout.add(db):
                        total_imported_workouts += 1
        logger.info("{} workouts fetched and {} workouts imported".format(
            total_fetched_workouts, total_imported_workouts))
        return(total_fetched_workouts, total_imported_workouts)
