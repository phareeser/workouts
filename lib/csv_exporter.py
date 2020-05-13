# coding=utf-8

from lib.workout_exporter import WorkoutExporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 
import logging
import csv

logger = logging.getLogger(__name__)


class CsvExporter(WorkoutExporter):
  def __init__(self, filename):
    logger.info("csv exporter initializing ...")
    self.csv = None
    self.filename = filename    
  
  def create_session(self):
    logger.info("csv exporter creating session ...")
    self.csv = open(self.filename, 'w', encoding='utf-8', newline='')

  def close_session(self):
    logger.info("csv exporter closing session ...")
    if self.csv:
      self.csv.close()
    self.csv = None

  def export_workouts(self, db):
    logger.info("exporting workouts ...")
    exported_workouts = 0
    workouts = db.session.query(Workout).all()
    csv_data = []

    #header line
    header = Workout.header(db)
    csv_data.append(header)
    # record lines
    for workout in workouts:
      csv_data.append(workout.as_list(db))
      exported_workouts += 1
    writer = csv.writer(self.csv)
    writer.writerows(csv_data)
    logger.info("{} workouts exported".format(exported_workouts))
