# coding=utf-8

import logging
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy import ForeignKey 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Sport(Base):
  __tablename__ = 'sports'
  id          = Column(Integer, primary_key = True)
  name        = Column(String)
  sportstypes = relationship('SportsType')
  workouts    = relationship('Workout') 

class SportsType(Base):
  __tablename__ = 'sportstypes'
  id        = Column(Integer, primary_key = True)
  name      = Column(String)
  sport_id  = Column(Integer, ForeignKey('sports.id'))
  workouts  = relationship("Workout")


class Workout(Base):
  __tablename__ = 'workouts'
  
  id            = Column(Integer, primary_key = True)
  source        = Column(String(32))
  source_ref    = Column(Integer) 
  sportstype_id = Column(Integer, ForeignKey('sportstypes.id'))
  sport_id      = Column(Integer, ForeignKey('sports.id'))
  name          = Column(String) 
  date          = Column(Date)

  def __repr__(self):
    return "{} '{}' from {}".format(self.sportstype, self.name, self.startdatetime)

  def close(self):
    pass


class WorkoutsDatabase:
  def __init__(self, database):
    engine = create_engine('sqlite:///{}'.format(database), echo=False)
    logging.info("connecting to {}".format(database))
    Session = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
    self.session = Session()

  def close(self):
    self.session.commit()
    self.session.close()  
  
  def add_if_not_exists(self, object):
    if isinstance(object, Sport):
      if not self.session.query(Sport.id).filter(Sport.name == object.name).first():
        logging.info("Adding new sport '{}'".format(object.name))
        self.session.add(object)
        return True
      return False
    elif isinstance(object, SportsType):
      if not self.session.query(SportsType.id).filter(SportsType.name == object.name).first():
        sport = Sport()
        if object.name in ['Race Bike', 'MTB', 'Trekking Bike']:
          sport.name = "Bike"
        elif object.name in ['Cross Running', 'Street Running']:
          sport.name = "Running"
        else: 
          sport.name = object.name
        self.add_if_not_exists(sport)
        object.sport_id = self.session.query(Sport.id).filter(Sport.name == sport.name).first()[0]
        logging.info("Adding new sportstype '{}' for sport '{}' (id {})".format(object.name, sport.name, object.sport_id))
        self.session.add(object)
        return True
      return False
    elif isinstance(object, Workout):
      if not self.session.query(Workout.id).filter(Workout.name == object.name).first():
        logging.info("Adding new workout '{}'".format(object.name))
        self.session.add(object)
        return True
      return False
    else:
      return False





"""
  def _to_workout(workout)  
    activity = Activity.new
    activity.record[:source] = "garmin"
    activity.record[:id] = garmin["activityId"]
    activity.record[:name]  = garmin["activityName"]
    activity.record[:description]  = garmin["description"]
    activity.record[:start_time]  = garmin["startTimeLocal"]
    activity.record[:sport_type]  = garmin["activityType.typeKey"]
    activity.record[:comments] = garmin["comments"]
    activity.record[:parent_id] = garmin["parentId"]
    activity.record[:distance] = garmin["distance"].to_i
    activity.record[:duration] = garmin["duration"] ? (garmin["duration"].to_i/60) : garmin["duration"]
    activity.record[:moving_duration] = garmin["movingDuration"] ? (garmin["movingDuration"].to_i/60) : garmin["movingDuration"]
    activity.record[:elevation_gain] = garmin["elevationGain"].to_i
    activity.record[:elevation_loss] = garmin["elevationLoss"].to_i
    activity.record[:average_speed] = garmin["averageSpeed"] ? (garmin["averageSpeed"] * 3.6).to_f.round(2) : garmin["averageSpeed"]
    activity.record[:max_speed] = garmin["maxSpeed"] ? (garmin["maxSpeed"] * 3.6).to_f.round(2) : garmin["maxSpeed"]
    activity.record[:calories] = garmin["calories"].to_i
    activity.record[:average_hr] = garmin["averageHR"].to_i
    activity.record[:max_hr] = garmin["maxHR"].to_i
    activity.record[:average_running_cadence_in_steps_per_minute] = garmin["averageRunningCadenceInStepsPerMinute"].to_i
    activity.record[:max_running_cadence_in_steps_per_minute] = garmin["maxRunningCadenceInStepsPerMinute"].to_i
    activity.record[:average_biking_cadence_in_rev_per_minute] = garmin["averageBikingCadenceInRevPerMinute"].to_i
    activity.record[:max_biking_cadence_in_rev_per_minute] = garmin["maxBikingCadenceInRevPerMinute"].to_i
    activity.record[:average_swim_cadence_in_strokes_per_minute] = garmin["averageSwimCadenceInStrokesPerMinute"].to_i
    activity.record[:max_swim_cadence_in_strokes_per_minute] = garmin["maxSwimCadenceInStrokesPerMinute"].to_i
    activity.record[:average_swolf] = garmin["averageSwolf"].to_i
    activity.record[:active_lengths] = garmin["activeLengths"].to_i
    activity.record[:pool_length] = garmin["poolLength"].to_i
    activity.record[:unit_of_pool_length] = garmin["unitOfPoolLength"].to_i
    activity.record[:avg_power] = garmin["avgPower"].to_i
    activity.record[:max_power] = garmin["maxPower"].to_i
    activity.record[:aerobic_training_effect] = garmin["aerobicTrainingEffect"].to_f.round(1)
    activity.record[:anaerobic_training_effect] = garmin["anaerobicTrainingEffect"].to_f.round(1)
    activity.record[:strokes] = garmin["strokes"].to_i
    activity.record[:norm_power] = garmin["normPower"].to_i
    activity.record[:left_balance] = garmin["leftBalance"]
    activity.record[:right_balance] = garmin["rightBalance"]
    activity.record[:avg_left_balance] = garmin["avgLeftBalance"]
    activity.record[:max_20_min_power] = garmin["max20MinPower"].to_i
    activity.record[:avg_vertical_oscillation] = garmin["avgVerticalOscillation"].to_f.round(2)
    activity.record[:avg_ground_contact_time] = garmin["avgGroundContactTime"].to_i
    activity.record[:avg_stride_length] = garmin["avgStrideLength"].to_i
    activity.record[:avg_fractional_cadence] = garmin["avgFractionalCadence"].to_i
    activity.record[:max_fractional_cadence] = garmin["maxFractionalCadence"].to_i
    activity.record[:training_stress_score] = garmin["trainingStressScore"].to_i
    activity.record[:intensity_factor] = garmin["intensityFactor"].to_i
    activity.record[:vo2_max_value] = garmin["vO2MaxValue"].to_i
    activity.record[:avg_vertical_ratio] = garmin["avgVerticalRatio"].to_i
    activity.record[:avg_ground_contact_balance] = garmin["avgGroundContactBalance"].to_i
    activity.record[:lactate_threshold_bpm] = garmin["lactateThresholdBpm"].to_i
    activity.record[:lactate_threshold_speed] = garmin["lactateThresholdSpeed"].to_i
    activity.record[:max_ftp] = garmin["maxFtp"].to_i
    activity.record[:avg_stroke_distance] = garmin["avgStrokeDistance"].to_i
    activity.record[:avg_stroke_cadence] = garmin["avgStrokeCadence"].to_i
    activity.record[:max_stroke_cadence] = garmin["maxStrokeCadence"].to_i
    activity.record[:avg_strokes] = garmin["avgStrokes"].to_i
    activity.record[:min_strokes] = garmin["minStrokes"].to_i
    activity.record[:min_temperature] = garmin["minTemperature"].to_f.round(1)
    activity.record[:max_temperature] = garmin["maxTemperature"].to_f.round(1)
    activity.record[:max_avg_power_1] = garmin["maxAvgPower_1"]
    activity.record[:max_avg_power_2] = garmin["maxAvgPower_2"]
    activity.record[:max_avg_power_5] = garmin["maxAvgPower_5"]
    activity.record[:max_avg_power_10] = garmin["maxAvgPower_10"]
    activity.record[:max_avg_power_20] = garmin["maxAvgPower_20"]
    activity.record[:max_avg_power_30] = garmin["maxAvgPower_30"]
    activity.record[:max_avg_power_60] = garmin["maxAvgPower_60"]
    activity.record[:max_avg_power_120] = garmin["maxAvgPower_120"]
    activity.record[:max_avg_power_300] = garmin["maxAvgPower_300"]
    activity.record[:max_avg_power_600] = garmin["maxAvgPower_600"]
    activity.record[:max_avg_power_1200] = garmin["maxAvgPower_1200"]
    activity.record[:max_avg_power_1800] = garmin["maxAvgPower_1800"]
    activity.record[:max_avg_power_3600] = garmin["maxAvgPower_3600"]
    activity.record[:max_avg_power_7200] = garmin["maxAvgPower_7200"]
    activity.record[:max_avg_power_18000] = garmin["maxAvgPower_18000"]
"""
