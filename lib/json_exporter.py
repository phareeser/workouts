# coding=utf-8

from lib.workout_exporter import WorkoutExporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 
import logging
import json

logger = logging.getLogger(__name__)


class JsonExporter(WorkoutExporter):
  def __init__(self, filename):
    logger.info("json exporter initializing ...")
    self.json = None
    self.filename = filename    
  
  def create_session(self):
    logger.info("json exporter creating session ...")
    self.json = open(self.filename, 'w', encoding='utf-8')

  def close_session(self):
    logger.info("json exporter closing session ...")
    if self.json:
      self.json.close()
    self.json = None

  def export_workouts(self, db):
    logger.info("exporting workouts ...")
    exported_workouts = 0
    workouts = db.session.query(Workout).all()
    json_data = []
    for workout in workouts:
      json_data.append(workout.as_dict(db))
      exported_workouts += 1
    json.dump(json_data, self.json)
    logger.info("{} workouts exported".format(exported_workouts))
