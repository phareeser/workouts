# coding=utf-8

import logging
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine, or_, and_, func
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
logger = logging.getLogger(__name__)

class Sport(Base):
    """
    Class manages Sport model
    Sport is the generic description of a SportsType: e.g. Sport is 'Cycling' for SportsType 'Montainbiking'
    rferenced by models SportsType and Workout
    - 'add' a sport record to the database
    """
    __tablename__ = 'sports'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sportstypes = relationship('SportsType')
    workouts = relationship('Workout')

    def add(self, database):
        id = database.session.query(Sport.id).filter(
            Sport.name == self.name).first()
        if id:
            self.id = id[0]
            return False
        else:
            database.session.add(self)
            database.session.flush()
            logger.info("Added new sport '{}' id {}".format(self.name, self.id))
            return True

    def __repr__(self):
        return "({}) {}".format(self.id, self.name)


class SportsType(Base):
    """
    Class manages SportsType model
    SportsType is a specific description of an activity, e.g. 'Treadmill Running', whereas the Sport is more generic 'Running'
    referenced by model Workout
    referencing model Sport
    - 'add' a sportstype record to the database
    - 'associate_sport' identifies the generic sport and creates a new sport record if not existing
    - 'cleanup_sportstype modifies the name of the sportstype to achieve a unified form when imported with different names with the same meaning
    """
    __tablename__ = 'sportstypes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sport_id = Column(Integer, ForeignKey('sports.id'))
    workouts = relationship("Workout")

    def associate_sport(self, database):
        sport = Sport()
        if self.name.lower() in ['indoor_cycling', 'indoor cycling', 'virtual_ride', 'cycling', 'road_biking', 'outdoor_cycling', 'road cycling', 'cross cycling', 'offroad cycling', 'mountain_biking', 'mountain biking']:
            sport.name = "Cycling"
        elif self.name.lower() in ['running', 'Trail Running', 'Street Running', 'treadmill_running', 'treadmill running', 'trail_running', 'trail running']:
            sport.name = "Running"
        elif self.name.lower() in ['lap_swimming', 'pool swimming', 'swimming', 'open water swimming']:
            sport.name = 'Swimming'
        elif self.name.lower() in ['cardio', 'indoor_cardio']:
            sport.name = 'Cardio'
        elif self.name.lower() in ['strength_training', 'strength']:
            sport.name = 'Strength'
        elif self.name.lower() in ['hiking']:
            sport.name = 'Hiking'
        elif self.name.lower() in ['yoga']:
            sport.name = 'Yoga'
        elif self.name.lower() in ['inline_skating', 'inline hockey']:
            sport.name = 'Inline Skating'
        elif self.name.lower() in ['multi_sport', 'triathlon']:
            sport.name = 'Triathlon'
        elif self.name.lower() in ['wakeboarding']:
            sport.name = 'Wakeboarding'
        elif self.name.lower() in ['surfing']:
            sport.name = 'Surfing'
        elif self.name.lower() in ['other']:
            sport.name = 'Other'
        else:
            sport.name = self.name

        sport.add(database)
        self.sport_id = sport.id

    def cleanup_sportstype(self, workout):
        if self.name.lower() in ['indoor_cycling', 'virtual_ride']:
            self.name = 'Indoor Cycling'
        elif self.name.lower() in ['cycling', 'road_biking']:
            self.name = 'Road Cycling'
        elif self.name.lower() in ['mountain_biking']:
            self.name = 'Mountain Biking'
        elif self.name.lower() in ['running']:
            self.name = 'Running'
        elif self.name.lower() in ['treadmill_running']:
            self.name = 'Treadmill Running'
        elif self.name.lower() in ['trail_running']:
            self.name = 'Trail Running'
        elif self.name.lower() in ['lap_swimming', 'swimming']:
            self.name = 'Pool Swimming'
        elif self.name.lower() in ['open_water_swimming']:
            self.name = 'Open Water Swimming'
        elif self.name.lower() in ['cardio', 'indoor_cardio']:
            self.name = 'Cardio'
        elif self.name.lower() in ['strength_training']:
            self.name = 'Strength'
        elif self.name.lower() in ['hiking']:
            self.name = 'Hiking'
        elif self.name.lower() in ['yoga']:
            self.name = 'Yoga'
        elif self.name.lower() in ['inline_skating', 'inline hockey']:
            self.name = 'Inline Skating'
        elif self.name.lower() in ['multi_sport']:
            self.name = 'Triathlon'
        elif self.name.lower() in ['wakeboarding']:
            self.name = 'Wakeboarding'
        elif self.name.lower() in ['surfing']:
            self.name = 'Surfing'
        elif self.name.lower() in ['other']:
            if workout.name:
                if workout.name == 'Yoga':
                    self.name = 'Yoga'
                if workout.name == 'Inline Hockey':
                    self.name = 'Inline Skating'
                if workout.name == 'Radfahren':
                    self.name = 'Road Cycling'
            else:
                self.name = 'Other'

    def add(self, workout, database):
        self.cleanup_sportstype(workout)
        self.associate_sport(database)
        id = database.session.query(SportsType.id).filter(
            SportsType.name == self.name).first()
        if id:
            self.id = id[0]
            return False
        else:
            database.session.add(self)
            database.session.flush()
            logger.info("Adding new sportstype '{}' id {} of sport {}".format(
                self.name, self.id, self.sport_id))
            return True

    def __repr__(self):
        return "({}) {} of type {}".format(self.id, self.name, self.sport_id)


class Workout(Base):
    """
    Class manages Workout model
    Workout contains all summary information of a sports activity
    referencing models Sport and Sportstype
    - 'add' a workout record to the database
    - 'as_dict' returns a dictionary representation of a workout instance
    - 'as_list' returns a list representation of a workout instance
    - 'header' returns a list of all attributes
    """
    __tablename__ = 'workouts'

    # identification
    id = Column(Integer, primary_key=True)
    source = Column(String(32))
    external_id = Column(Integer)

    # organisational
    is_duplicate_with = Column(Integer)
    manual_check_required_with = Column(Integer)

    # sportstype
    sportstype_id = Column(Integer, ForeignKey('sportstypes.id'))
    sport_id = Column(Integer, ForeignKey('sports.id'))
    # description
    name = Column(String)
    description = Column(String)
    # time
    start_time = Column(DateTime)
    duration_sec = Column(Integer)
    moving_duration_sec = Column(Integer)
    # conditions
    min_temperature = Column(Integer)
    max_temperature = Column(Integer)
    # key performance indicators
    distance_m = Column(Integer)
    average_speed_m_per_sec = Column(Float)
    max_speed_m_per_sec = Column(Float)
    calories = Column(Integer)
    average_hr = Column(Integer)
    max_hr = Column(Integer)
    avg_power = Column(Integer)
    max_power = Column(Integer)
    norm_power = Column(Integer)
    elevation_gain_m = Column(Integer)
    elevation_loss_m = Column(Integer)
    # training effect
    aerobic_training_effect = Column(Float)
    anaerobic_training_effect = Column(Float)
    training_stress_score = Column(Float)
    intensity_factor = Column(Float)
    # cadences
    average_running_cadence_steps_per_min = Column(Integer)
    max_running_cadence_steps_per_min = Column(Integer)
    average_biking_cadence_rev_per_min = Column(Integer)
    max_biking_cadence_rev_per_min = Column(Integer)
    average_swim_cadence_strokes_per_min = Column(Integer)
    max_swim_cadence_strokes_per_min = Column(Integer)
    # running specific
    left_balance = Column(Float)
    right_balance = Column(Float)
    avg_left_balance = Column(Float)
    avg_vertical_oscillation = Column(Float)
    avg_ground_contact_time = Column(Integer)
    avg_stride_length = Column(Integer)
    avg_fractional_cadence = Column(Integer)
    max_fractional_cadence = Column(Integer)
    avg_vertical_ratio = Column(Float)
    avg_ground_contact_balance = Column(Float)
    # swimming specific
    average_swolf = Column(Integer)
    active_lengths = Column(Integer)
    pool_length = Column(Integer)
    unit_of_pool_length = Column(String)
    pool_length_factor = Column(Integer)
    strokes = Column(Integer)
    avg_stroke_distance = Column(Integer)
    avg_stroke_cadence = Column(Integer)
    max_stroke_cadence = Column(Integer)
    avg_strokes = Column(Float)
    min_strokes = Column(Float)
    # fitness level
    vo2_max_value = Column(Integer)
    lactate_threshold_bpm = Column(Integer)
    lactate_threshold_speed = Column(Integer)
    max_ftp = Column(Integer)
    max_20_min_power = Column(Integer)
    max_avg_power_1 = Column(Integer)
    max_avg_power_2 = Column(Integer)
    max_avg_power_5 = Column(Integer)
    max_avg_power_10 = Column(Integer)
    max_avg_power_20 = Column(Integer)
    max_avg_power_30 = Column(Integer)
    max_avg_power_60 = Column(Integer)
    max_avg_power_120 = Column(Integer)
    max_avg_power_300 = Column(Integer)
    max_avg_power_600 = Column(Integer)
    max_avg_power_1200 = Column(Integer)
    max_avg_power_1800 = Column(Integer)
    max_avg_power_3600 = Column(Integer)
    max_avg_power_7200 = Column(Integer)
    max_avg_power_18000 = Column(Integer)

    def __repr__(self):
        return "{} | {} | {} | {} | {} | dup:{} | check:{} | "\
            .format(self.id, self.source, self.name, self.start_time, self.sport_id, self.is_duplicate_with, self.manual_check_required_with)

    def as_dict(self, db):
        dict = {}
        for column in self.__table__.columns:
            key = column.name
            if key in ["id", "sport_id", "is_duplicate_with", "manual_check_required_with"]:
                continue
            elif key == "external_id":
                value = getattr(self, key)
                key = "id"
            elif key == "start_time":
                value = str(getattr(self, key))
            elif key == "sportstype_id":
                value = db.session.query(SportsType.name).filter(
                    SportsType.id == getattr(self, key)).first()[0]
                key = "sportstype"
            else:
                value = getattr(self, key)
            dict[key] = value
        return dict

    def as_list(self, db):
        # returns a list of all workout attributes
        keys = self.__table__.columns.keys()
        list = []
        for key in keys:
            if key in ["external_id", "sport_id", "is_duplicate_with", "manual_check_required_with"]:
                continue
            elif key == "id":
                list.append(getattr(self, "external_id"))
            elif key == "sportstype_id":
                list.append(db.session.query(SportsType.name).filter(
                    SportsType.id == getattr(self, key)).first()[0])
            else:
                list.append(getattr(self, key))
        return list

    @classmethod
    def header(cls, database):
        keys = cls.__table__.columns.keys()
        for i in range(len(keys)):
            if keys[i] == "sportstype_id":
                keys[i] = "sportstype"
                break
        keys.remove("is_duplicate_with")
        keys.remove("manual_check_required_with")
        keys.remove("external_id")
        keys.remove("sport_id")
        return keys

    def _merge_attributes(self, copied_workout):
        '''
        Merging attributes from copied_workout to self, 
        if the attributes are not populated yet or seem odd for other reasons
        '''
        # returns a list of all workout attributes
        keys = self.__table__.columns.keys()
        for key in keys:
            if key in ["id",
                       "external_id",
                       "is_duplicate_with",
                       "manual_check_required_with",
                      ]:
                continue
            elif getattr(self, key) == None:
                setattr(self, key, getattr(copied_workout, key))


    def handle_duplicates(self, database):
        '''
        If a workout seems to be known in the database, for example because already imported from another source,
        create a new workout and mark the others as duplicate.
        Populate the new workout with the most appropriate information of all duplicates 
        Used attributes:
            is_duplicate_with = Column(Integer)    => reference to the leading workout
            manual_check_reqired = Column(Boolean) => if automated cleaning is not possible
        '''
        number_of_duplicates = 0
        number_of_merged = 0
        
        # return if this workout is a merged workout
        if self.source == "MERGED WORKOUT":
            logger.debug("dup check - no check, since this workout is merged: {}".format(self))
            return (number_of_duplicates, number_of_merged)

        # return if this workout already has been checked
        if self.is_duplicate_with or self.manual_check_required_with:
            logger.debug("dup check - no check, since this workout is marked: {}".format(self))
            return (number_of_duplicates, number_of_merged)

        # return if this workout does not have start_time set, since the following checks are based on it
        if not self.start_time or not self.duration_sec:
            return (number_of_duplicates, number_of_merged)

        # potential duplicate if time is overlapping
        # this workout                          |-----------------|
        # 1st potential duplicate in db     |-----------------|
        # 2nd potential duplicate in db     |------------------------|
        # 3rd potential duplicate in db             |----------------|
        # 4th potential duplicate in db             |---------|
        # (Remark to line 2 of 1st filter: needed to use database functions, 
        # because modifiers like timedelta do not work with sqlalchemy sql attributes)
        # TODO handle timezones (needed for sqlite strftime)
        duplicates = database.session.query(Workout)\
            .filter(or_(and_(Workout.start_time < self.start_time,
                             func.strftime('%s', Workout.start_time, 'utc') + Workout.duration_sec >= self.start_time.timestamp()),
                        and_(Workout.start_time >= self.start_time,
                             Workout.start_time < (self.start_time + datetime.timedelta(seconds=int(self.duration_sec))))))\
            .filter(Workout.is_duplicate_with == None)\
            .filter(Workout.manual_check_required_with == None)\
            .filter(Workout.id != self.id)\
            .all()

        if len(duplicates) == 0:
            return (number_of_duplicates, number_of_merged)

        # find overlapping workouts of different sports -> set manual_check_required_with
        for duplicate in duplicates:
            if duplicate.sport_id != self.sport_id:
                self.manual_check_required_with = duplicate.id
                logger.debug("dup check - workout marked to be checked: {}".format(duplicate))
                duplicates.remove(duplicate)
        if len(duplicates) == 0:
            return (number_of_duplicates, number_of_merged)

        # find overlapping workouts of same sports (they are duplicate workouts) -> now find the leading workout
        leading_workout = None
        # Step 1: if one of the duplicates is a previously merged one, use it as the leading workout
        for duplicate in duplicates:
            if duplicate.source and duplicate.source == "MERGED WORKOUT":
                leading_workout = duplicate
        # Step 2: else if one of the duplicates is from Zwift, prefer it as the leading workout
        if not leading_workout:
            for duplicate in duplicates:
                if duplicate.name and "Zwift" in duplicate.name:
                    leading_workout = duplicate
        # Step 3: else if one of the duplicates is a Garmin import, prefer it as the leading workout
        if not leading_workout:
            for duplicate in duplicates:
                if duplicate.source and "Garmin" in duplicate.source:
                    leading_workout = duplicate
        # Step 4: else use this workout as the leading workout
        if not leading_workout:
            leading_workout = self
        logger.debug("dup check - leading workout is: {}".format(leading_workout))

        # create a new workout that will be treated as the leading one. Mark the duplicates 
        if leading_workout.source == "MERGED WORKOUT":
            merged_workout = leading_workout
        else:
            merged_workout = Workout(source="MERGED WORKOUT", external_id=datetime.datetime.now().timestamp())
            merged_workout._merge_attributes(leading_workout)
            logger.debug("dup check - merged workout with leading: {}".format(merged_workout))
            merged_workout.add(database)
            leading_workout.is_duplicate_with = merged_workout.id
            number_of_merged += 1
        if self is not leading_workout:
            merged_workout._merge_attributes(self)
            logger.debug("dup check - merged workout with self: {}".format(merged_workout))
        self.is_duplicate_with = merged_workout.id
        number_of_duplicates += 1
        for duplicate in duplicates:
            if duplicate is leading_workout:
                continue
            merged_workout._merge_attributes(duplicate)
            logger.debug("dup check - merged workout duplicate: {}".format(merged_workout))
            duplicate.is_duplicate_with = merged_workout.id
            number_of_duplicates += 1
            logger.debug("dup check - duplicate workout marked: {}".format(duplicate))
        return (number_of_duplicates, number_of_merged)


    def add(self, database):
        # don't add if this workout has already been added
        id = database.session.query(Workout.id) \
            .filter(Workout.external_id == self.external_id) \
            .filter(Workout.source == self.source) \
            .first()
        if id:
            return False
        else:
            database.session.add(self)
            database.session.flush()
            logger.info("Added new workout {}".format(self))
            self.handle_duplicates(database)
            return True


class WorkoutsDatabase:
    """
    Class handles SQLite DB session and manages functions that comprise the whole database rather than distinct records
    - create database
    - create session
    - close session
    - show all records of the database
    - cleanup database
    """
    def __init__(self, database):
        engine = create_engine('sqlite:///{}'.format(database), echo=False)
        logger.info("connecting to {}".format(database))
        Session = sessionmaker(bind=engine)
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

    def check(self):
        ''' Database cleanup
            Check for duplicate workouts
            If duplicates are detected, use the most reliable information and mark the duplicate workouts 

            Duplicate detection:
                - If workouts are overlapping in time, further checks are required
                    - If they are of the same sportstype, then they are duplicates
                    - If they are of different sportstype, then "manual_check_required_with" will be set

            Cleansing of duplicates:
                1. create a new workout
                2. mark the original workout as duplicates and add a reference in "is_duplicate_with"
                3. decide for the more reliable record:
                    1. source == Garmin is preferred
                    2. the workout with the better average speed is preferred
                4. update the new workout with the attributes of the preferred duplicate workout
                5. update the new workout with the attributes of the not preferred workout, if this attribute is not yet set
            
        '''
        number_of_checked_workouts = 0
        number_of_merged_workouts = 0
        number_of_duplicate_workouts = 0        
        workouts = self.session.query(Workout).all()
        for workout in workouts:
            number_of_checked_workouts += 1
            (a, b) = workout.handle_duplicates(self)
            number_of_duplicate_workouts += a
            number_of_merged_workouts += b
        logger.info('{} workouts checked, {} of them were duplicate, created {} merged workouts'\
            .format(number_of_checked_workouts,
                    number_of_duplicate_workouts,
                    number_of_merged_workouts,))
