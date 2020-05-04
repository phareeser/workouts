# coding=utf-8

from lib.workout_importer import WorkoutImporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 
import logging
import json
from datetime import datetime

class JsonImporter(WorkoutImporter):
  def __init__(self, filename):
    logging.info("json importer initializing ...")
    self.json = None
    self.filename = filename    
  
  def create_session(self):
    logging.info("json importer creating session ...")
    self.json = open(self.filename, "r")
  
  def close_session(self):
    logging.info("json importer closing session ...")
    if self.json:
      self.json.close()
    self.json = None

  def import_workouts(self, db):
    logging.info("fetching workouts ...")
    total_fetched_workouts = 0
    total_imported_workouts = 0
    for data in self.json:
      workouts = json.loads(data)
      for record in workouts:
        workout = Workout()
        total_fetched_workouts += 1
        for key in record:
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
        if 'source' not in record:
          workout.source = "JSON import"
        if workout.add(db):
          total_imported_workouts += 1
    logging.info("{} workouts fetched and {} workouts imported".format(total_fetched_workouts, total_imported_workouts))


