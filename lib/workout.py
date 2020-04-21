# coding=utf-8

import logging
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Numeric, DateTime
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

  def get(self, database, name):
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
    sport = Sport()
    if self.name in ['Race Bike', 'MTB', 'Trekking Bike']:
      sport.name = "Bike"
    elif self.name in ['Trail Running', 'Street Running']:
      sport.name = "Running"
    else: 
      sport.name = self.name
    return sport    
 
  def add(self, database):
    id = database.session.query(SportsType.id).filter(SportsType.name == self.name).first()
    if id:
      id = id[0]
    else:
      sport = self.associate_sport()
      self.sport_id = sport.add(database)
      logging.info("Adding new sportstype '{}'".format(self.name))
      database.session.add(self)
      database.session.flush()
      id = self.id
    return id

  def get(self, database, name):
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
  min_temperature                       = Column(Numeric, precision=4, scale=1)
  max_temperature                       = Column(Numeric, precision=4, scale=1)
  # time
  start_time                            = Column(DateTime)
  duration_sec                          = Column(Integer)
  moving_duration_sec                   = Column(Integer)
  # key performance indicators
  distance_m                            = Column(Integer)
  average_speed_m_per_sec               = Column(Numeric, precision=7, scale=2)
  max_speed_m_per_sec                   = Column(Numeric, precision=7, scale=2)
  elevation_gain_m                      = Column(Integer)
  elevation_loss_m                      = Column(Integer)
  calories                              = Column(Integer)
  average_hr                            = Column(Integer)
  max_hr                                = Column(Integer)
  avg_power                             = Column(Integer)
  max_power                             = Column(Integer)
  norm_power                            = Column(Integer)
  # training effect
  aerobic_training_effect               = Column(Numeric, precision=4, scale=1)
  anaerobic_training_effect             = Column(Numeric, precision=4, scale=1)
  training_stress_score                 = Column(Integer)
  intensity_factor                      = Column(Integer)
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
  unit_of_pool_length                   = Column(Integer)
  strokes                               = Column(Integer)
  avg_stroke_distance                   = Column(Integer)
  avg_stroke_cadence                    = Column(Integer)
  max_stroke_cadence                    = Column(Integer)
  avg_strokes                           = Column(Integer)
  min_strokes                           = Column(Integer)
  # running specific
  left_balance                          = Column(Numeric, precision=5, scale=2)
  right_balance                         = Column(Numeric, precision=5, scale=2)
  avg_left_balance                      = Column(Numeric, precision=5, scale=2)
  avg_vertical_oscillation              = Column(Numeric, precision=5, scale=2)
  avg_ground_contact_time               = Column(Integer)
  avg_stride_length                     = Column(Integer)
  avg_fractional_cadence                = Column(Integer)
  max_fractional_cadence                = Column(Integer)
  avg_vertical_ratio                    = Column(Integer)
  avg_ground_contact_balance            = Column(Integer)
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
    id = database.session.query(Workout.id).filter(Workout.name == self.name).first()
    if id:
      id = id[0]
    else:
      logging.info("Adding new workout '{}'".format(self.name))
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

  

