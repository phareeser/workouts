# coding=utf-8

import logging
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Float
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

  def add(self, database):
    id = database.session.query(Sport.id).filter(Sport.name == self.name).first()
    if id:
      id = id[0]
    else:
      logging.info("Adding new sport '{}'".format(self.name))
      database.session.add(self)
      database.session.flush()
      id = self.id
    return id

  @classmethod
  def get(cls, database, name):
    result = database.session.query(Sport).filter(Sport.name == name).all()
    if result:
      return result[0]
    else:
      return None

  def __repr__(self):
    return "({}) {}".format(self.id, self.name)



class SportsType(Base):
  __tablename__ = 'sportstypes'
  id        = Column(Integer, primary_key = True)
  name      = Column(String)
  sport_id  = Column(Integer, ForeignKey('sports.id'))
  workouts  = relationship("Workout")

  def associate_sport(self):
    name = None
    if self.name in ['indoor_cycling', 'indoor cycling', 'virtual_ride', 'cycling', 'road_biking', 'outdoor_cycling', 'road cycling', 'cross cycling', 'offroad cycling', 'mountain_biking', 'mountain biking']:
      name = "cycling"
    elif self.name in ['running', 'Trail Running', 'Street Running', 'treadmill_running', 'treadmill running', 'trail_running', 'trail running']:
      name = "running"
    elif self.name in ['lap_swimming', 'pool swimming', 'swimming', 'open water swimming']:
      name = 'swimming'
    elif self.name in ['cardio', 'indoor_cardio']:
      name = 'cardio'
    elif self.name in ['strength_training', 'strength']:
      name = 'strength'
    elif self.name in ['hiking']:
      name = 'hiking'
    elif self.name in ['yoga']:
      name = 'yoga'
    elif self.name in ['inline_skating', 'inline hockey']:
      name = 'inline skating'
    elif self.name in ['multi_sport', 'triathlon']:
      name = 'triathlon'    
    elif self.name in ['wakeboarding']:
      name = 'wakeboarding'    
    elif self.name in ['other']:
      name = 'other'    
    else: 
      name = self.name
    return name    
 
  def cleanup_sportstype(self):
    if self.name in ['indoor_cycling', 'virtual_ride']:
      self.name = 'indoor cycling'
    elif self.name in ['cycling', 'road_biking']:
      self.name = 'road cycling'
    elif self.name in ['mountain_biking']:
      self.name = 'mountain biking'
    elif self.name in ['running']:
      self.name = 'running'
    elif self.name in ['treadmill_running']:
      self.name = 'treadmill running'
    elif self.name in ['trail_running']:
      self.name = 'trail running'
    elif self.name in ['lap_swimming', 'swimming']:
      self.name = 'pool swimming'
    elif self.name in ['open_water_swimming']:
      self.name = 'open water swimming'
    elif self.name in ['cardio', 'indoor_cardio']:
      self.name = 'cardio'
    elif self.name in ['strength_training']:
      self.name = 'strength'
    elif self.name in ['hiking']:
      self.name = 'hiking'
    elif self.name in ['yoga']:
      self.name = 'yoga'
    elif self.name in ['inline_skating', 'inline hockey']:
      self.name = 'inline skating'
    elif self.name in ['multi_sport']:
      self.name = 'triathlon'    
    elif self.name in ['wakeboarding']:
      self.name = 'wakeboarding'    
    elif self.name in ['other']:
      self.name = 'other'    
    return self.name

  def add(self, database):
    self.name = self.cleanup_sportstype()
    self.sport_id = Sport(name = self.associate_sport()).add(database)
    id = database.session.query(SportsType.id).filter(SportsType.name == self.name).first()
    if id:
      id = id[0]
    else:
      database.session.add(self)
      database.session.flush()
      logging.info("Adding new sportstype '{} id {}'".format(self.name, self.id))
      id = self.id
    return id

  @classmethod
  def get(cls, database, name):
    result = database.session.query(SportsType).filter(SportsType.name == name).all()
    if result:
      return result[0]
    else:
      return None

  def __repr__(self):
    return "({}) {} belongs to {}".format(self.id, self.name, self.sport_id)


class Workout(Base):
  __tablename__ = 'workouts'
  
  # identification
  id                                    = Column(Integer, primary_key = True)
  source                                = Column(String(32))
  external_id                           = Column(Integer)
  # sportstype 
  sportstype_id                         = Column(Integer, ForeignKey('sportstypes.id'))
  sport_id                              = Column(Integer, ForeignKey('sports.id'))
  # description
  name                                  = Column(String) 
  description                           = Column(String)
  min_temperature                       = Column(Integer)
  max_temperature                       = Column(Integer)
  # time
  start_time                            = Column(DateTime)
  duration_sec                          = Column(Integer)
  moving_duration_sec                   = Column(Integer)
  # key performance indicators
  distance_m                            = Column(Integer)
  average_speed_m_per_sec               = Column(Float)
  max_speed_m_per_sec                   = Column(Float)
  elevation_gain_m                      = Column(Integer)
  elevation_loss_m                      = Column(Integer)
  calories                              = Column(Integer)
  average_hr                            = Column(Integer)
  max_hr                                = Column(Integer)
  avg_power                             = Column(Integer)
  max_power                             = Column(Integer)
  norm_power                            = Column(Integer)
  # training effect
  aerobic_training_effect               = Column(Float)
  anaerobic_training_effect             = Column(Float)
  training_stress_score                 = Column(Float)
  intensity_factor                      = Column(Float)
  # cadences
  average_running_cadence_steps_per_min = Column(Integer)
  max_running_cadence_steps_per_min     = Column(Integer)
  average_biking_cadence_rev_per_min    = Column(Integer)
  max_biking_cadence_rev_per_min        = Column(Integer)
  average_swim_cadence_strokes_per_min  = Column(Integer)
  max_swim_cadence_strokes_per_min      = Column(Integer)
  # swimming specific
  average_swolf                         = Column(Integer)
  active_lengths                        = Column(Integer)
  pool_length                           = Column(Integer)
  unit_of_pool_length                   = Column(String)
  pool_length_factor                    = Column(Integer)
  strokes                               = Column(Integer)
  avg_stroke_distance                   = Column(Integer)
  avg_stroke_cadence                    = Column(Integer)
  max_stroke_cadence                    = Column(Integer)
  avg_strokes                           = Column(Float)
  min_strokes                           = Column(Float)
  # running specific
  left_balance                          = Column(Float)
  right_balance                         = Column(Float)
  avg_left_balance                      = Column(Float)
  avg_vertical_oscillation              = Column(Float)
  avg_ground_contact_time               = Column(Integer)
  avg_stride_length                     = Column(Integer)
  avg_fractional_cadence                = Column(Integer)
  max_fractional_cadence                = Column(Integer)
  avg_vertical_ratio                    = Column(Float)
  avg_ground_contact_balance            = Column(Float)
  # fitness level
  vo2_max_value                         = Column(Integer)
  lactate_threshold_bpm                 = Column(Integer)
  lactate_threshold_speed               = Column(Integer)
  max_ftp                               = Column(Integer)
  max_20_min_power                      = Column(Integer)
  max_avg_power_1                       = Column(Integer)
  max_avg_power_2                       = Column(Integer)
  max_avg_power_5                       = Column(Integer)
  max_avg_power_10                      = Column(Integer)
  max_avg_power_20                      = Column(Integer)
  max_avg_power_30                      = Column(Integer)
  max_avg_power_60                      = Column(Integer)
  max_avg_power_120                     = Column(Integer)
  max_avg_power_300                     = Column(Integer)
  max_avg_power_600                     = Column(Integer)
  max_avg_power_1200                    = Column(Integer)
  max_avg_power_1800                    = Column(Integer)
  max_avg_power_3600                    = Column(Integer)
  max_avg_power_7200                    = Column(Integer)
  max_avg_power_18000                   = Column(Integer)

  def __repr__(self):
    return "({}) {} from {} doing {} ({}) imported by {}".format(self.id, self.name, self.date, self.sportstype_id, self.sport_id, self.source)

  def close(self):
    pass

  def add(self, database):
    id = database.session.query(Workout.id) \
      .filter(Workout.external_id == self.external_id) \
      .filter(Workout.source == self.source) \
      .first()
    if id:
      id = id[0]
    else:
      logging.info("Adding new workout '{}' with sportstype {}".format(self.name, self.sportstype_id))
      database.session.add(self)
      database.session.flush()
      id = self.id
    return id


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
  
  def showall(self):
    print("SPORTS:")
    sports = self.session.query(Sport).all()
    for sport in sports:
      print(sport)
    print("SPORTSTYPES:")
    sportstypes = self.session.query(SportsType).all()
    for sportstype in sportstypes:
      print(sportstype)
    print("WORKOUTS:")
    workouts = self.session.query(Workout).all()
    for workout in workouts:
      print(workout)

  

