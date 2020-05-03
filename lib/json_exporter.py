# coding=utf-8

from lib.workout_exporter import WorkoutExporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 
import logging
import json

class JsonExporter(WorkoutExporter):
  def __init__(self, filename):
    logging.info("json exporter initializing ...")
    self.json = None
    self.filename = filename    
  
  def create_session(self):
    logging.info("json exporter creating session ...")
    self.json = open(self.filename, 'w', encoding='utf-8')

  def close_session(self):
    logging.info("json exporter closing session ...")
    if self.json:
      self.json.close()
    self.json = None

  def export_workouts(self, db):
    logging.info("exporting workouts ...")
    workouts = db.session.query(Workout).all()
    json_data = []
    for workout in workouts:
      json_data.append(workout.as_dict(db))
    json.dump(json_data, self.json)
