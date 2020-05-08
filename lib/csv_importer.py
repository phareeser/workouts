# coding=utf-8

from lib.workout_importer import WorkoutImporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase
import logging
import csv
from datetime import datetime


class CsvImporter(WorkoutImporter):
    def __init__(self, filename):
        logging.info("csv importer initializing ...")
        self.csv = None
        self.filename = filename

    def create_session(self):
        logging.info("csv importer creating session ...")
        self.csv = open(self.filename, "r")

    def close_session(self):
        logging.info("csv importer closing session ...")
        if self.csv:
            self.csv.close()
        self.csv = None

    def import_workouts(self, db):
        logging.info("fetching workouts ...")
        total_fetched_workouts = 0
        total_imported_workouts = 0

        keys = Workout.header(db)
        workouts = csv.DictReader(self.csv)
        # TODO check if header is correct
        for record in workouts:
            logging.debug('CSV record: {}'.format(record))
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
                    sportstype.add(db)
                    workout.sportstype_id = sportstype.id
                    workout.sport_id = sportstype.sport_id
                    continue
                setattr(workout, key, record[key])
                if getattr(workout, key) == '':
                    setattr(workout, key, None)
                logging.debug('{} : {}'.format(key, getattr(workout, key)))
            if 'source' not in keys:
                workout.source = "CSV import"
            logging.debug('WORKOUT: {}'.format(workout))
            if workout.add(db):
                total_imported_workouts += 1

        logging.info("{} workouts fetched and {} workouts imported".format(
            total_fetched_workouts, total_imported_workouts))

