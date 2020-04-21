# coding=utf-8

from lib.workout_importer import WorkoutImporter
from lib.workout import Workout, Sport, SportsType, WorkoutsDatabase 
import logging
import json
import datetime

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
    for data in self.json:
      workouts = json.loads(data)
      for record in workouts:
        workout = Workout()
        workout.source = "JSON import"
        workout.external_id = record['activityId'] 
        workout.sport_id

        sport = record['activityType']['typeKey']
        sportstype = SportsType.get(db, sport)
        if not sportstype:
          sportstype = SportsType(name = sport)
          sportstype.add(db)
        workout.sportstype_id = sportstype.id
        workout.sport_id = Sport.get(db, sportstype.sport_id)

        workout.name = record['activityName']
        workout.description = record['description']
        workout.min_temperature = float(record['minTemperature']) if record['minTemperature'] else record['minTemperature']
        workout.max_temperature = float(record['maxTemperature']) if record['maxTemperature'] else record['maxTemperature']
        workout.start_time = datetime(record['startTimeLocal'])
        workout.duration_sec = int(record['duration'])/60
        workout.moving_duration_sec = int(record['movingDuration'])/60
        workout.distance_m = int(record['distance'])
        workout.average_speed_m_per_sec = float(record['averageSpeed']*3.6)
        workout.max_speed_m_per_sec = float(record['maxSpeed']*3.6) if record['maxSpeed'] else record['maxSpeed']
        workout.elevation_gain_m = int(record['elevationGain'])
        workout.elevation_loss_m = int(record['elevationLoss'])
        workout.calories = int(record['calories'])
        workout.average_hr = int(record['averageHR']) if record['averageHR'] else record['averageHR']
        workout.max_hr = int(record['maxHR']) if record['maxHR'] else record['maxHR']
        workout.avg_power = int(record['avgPower']) if record['avgPower'] else record['avgPower']
        workout.max_power = (record['maxPower'])
        workout.norm_power = (record['normPower'])
        workout.aerobic_training_effect = float(record['aerobicTrainingEffect']) if record['aerobicTrainingEffect'] else record['aerobicTrainingEffect']
        workout.anaerobic_training_effect = float(record['anaerobicTrainingEffect']) if record['anaerobicTrainingEffect'] else record['anaerobicTrainingEffect']
        workout.training_stress_score = (record['trainingStressScore'])
        workout.intensity_factor = (record['intensityFactor'])
        workout.average_running_cadence_steps_per_min = (record['averageRunningCadenceInStepsPerMinute'])
        workout.max_running_cadence_steps_per_min = (record['maxRunningCadenceInStepsPerMinute'])
        workout.average_biking_cadence_rev_per_min = (record['averageBikingCadenceInRevPerMinute'])
        workout.max_biking_cadence_rev_per_min = (record['maxBikingCadenceInRevPerMinute'])
        workout.average_swim_cadence_strokes_per_min = (record['averageSwimCadenceInStrokesPerMinute'])
        workout.max_swim_cadence_strokes_per_min = (record['maxSwimCadenceInStrokesPerMinute'])
        workout.average_swolf = (record['averageSwolf'])
        workout.active_lengths = (record['activeLengths'])
        workout.pool_length = (record['poolLength'])
        workout.unit_of_pool_length = (record['unitOfPoolLength'])
        workout.strokes = (record['strokes'])
        workout.avg_stroke_distance = (record['avgStrokeDistance'])
        workout.avg_stroke_cadence = (record['avgStrokeCadence'])
        workout.max_stroke_cadence = (record['maxStrokeCadence'])
        workout.avg_strokes = (record['avgStrokes'])
        workout.min_strokes = (record['minStrokes'])
        workout.left_balance = (record['leftBalance'])
        workout.right_balance = (record['rightBalance'])
        workout.avg_left_balance = (record['avgLeftBalance'])
        workout.avg_vertical_oscillation = float(record['avgVerticalOscillation']) if record['avgVerticalOscillation'] else record['avgVerticalOscillation']
        workout.avg_ground_contact_time = (record['avgGroundContactTime'])
        workout.avg_stride_length = (record['avgStrideLength'])
        workout.avg_fractional_cadence = (record['avgFractionalCadence'])
        workout.max_fractional_cadence = (record['maxFractionalCadence'])
        workout.avg_vertical_ratio = (record['avgVerticalRatio'])
        workout.avg_ground_contact_balance = (record['avgGroundContactBalance'])
        workout.vo2_max_value = (record['vO2MaxValue'])
        workout.lactate_threshold_bpm = (record['lactateThresholdBpm'])
        workout.lactate_threshold_speed = (record['lactateThresholdSpeed'])
        workout.max_ftp = (record['maxFtp'])
        workout.max_20_min_power = (record['max20MinPower'])
        workout.max_avg_power_1 = (record['maxAvgPower_1'])
        workout.max_avg_power_2 = (record['maxAvgPower_2'])
        workout.max_avg_power_5 = (record['maxAvgPower_5'])
        workout.max_avg_power_10 = (record['maxAvgPower_10'])
        workout.max_avg_power_20 = (record['maxAvgPower_20'])
        workout.max_avg_power_30 = (record['maxAvgPower_30'])          
        workout.max_avg_power_60 = (record['maxAvgPower_60'])
        workout.max_avg_power_120 = (record['maxAvgPower_120'])
        workout.max_avg_power_300 = (record['maxAvgPower_300'])
        workout.max_avg_power_600 = (record['maxAvgPower_600'])
        workout.max_avg_power_1200 = (record['maxAvgPower_1200'])
        workout.max_avg_power_1800 = (record['maxAvgPower_1800'])
        workout.max_avg_power_3600 = (record['maxAvgPower_3600'])
        workout.max_avg_power_7200 = (record['maxAvgPower_7200'])
        workout.max_avg_power_18000 = (record['maxAvgPower_18000'])
        workout.add(db)


# {'activityId': 4680052305, 'activityName': 'Mountainbike', 'description': None, 'startTimeLocal': '2020-03-21 13:16:58', 'startTimeGMT': '2020-03-21 12:16:58', 'activityType': {'typeId': 2, 'typeKey': 'cycling', 'parentTypeId': 17, 'sortOrder': 8}, 'eventType': {'typeId': 9, 'typeKey': 'uncategorized', 'sortOrder': 10}, 'comments': None, 'parentId': None, 'distance': 0.0, 'duration': 8523.291015625, 'elapsedDuration': 8523291.015625, 'movingDuration': 0.0, 'elevationGain': 0.0, 'elevationLoss': 0.0, 'averageSpeed': 0.0, 'maxSpeed': None, 'startLatitude': None, 'startLongitude': None, 'hasPolyline': False, 'ownerId': 12331285, 'ownerDisplayName': 'PhaReeseR', 'ownerFullName': 'PhaReeseR', 'ownerProfileImageUrlSmall': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/bc2e1cdc-ae07-40de-821e-3146441104e0-12331285.jpg', 'ownerProfileImageUrlMedium': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/738aef41-8b82-428e-8d48-aff5e9bbf498-12331285.jpg', 'ownerProfileImageUrlLarge': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/3764a7de-8073-46b5-b7be-cd88d7f62cdb-12331285.jpg', 'calories': 936.0, 'averageHR': 108.0, 'maxHR': 129.0, 'averageRunningCadenceInStepsPerMinute': None, 'maxRunningCadenceInStepsPerMinute': None, 'averageBikingCadenceInRevPerMinute': None, 'maxBikingCadenceInRevPerMinute': None, 'averageSwimCadenceInStrokesPerMinute': None, 'maxSwimCadenceInStrokesPerMinute': None, 'averageSwolf': None, 'activeLengths': None, 'steps': None, 'conversationUuid': None, 'conversationPk': None, 'numberOfActivityLikes': None, 'numberOfActivityComments': None, 'likedByUser': None, 'commentedByUser': None, 'activityLikeDisplayNames': None, 'activityLikeFullNames': None, 'requestorRelationship': None, 'userRoles': ['ROLE_CONNECTUSER', 'ROLE_FITNESS_USER', 'ROLE_WELLNESS_USER', 'ROLE_OUTDOOR_USER', 'ROLE_CONNECT_2_USER'], 'privacy': {'typeId': 2, 'typeKey': 'private'}, 'userPro': False, 'courseId': None, 'poolLength': None, 'unitOfPoolLength': None, 'hasVideo': False, 'videoUrl': None, 'timeZoneId': 124, 'beginTimestamp': 1584793018000, 'sportTypeId': 2, 'avgPower': None, 'maxPower': None, 'aerobicTrainingEffect': 2.299999952316284, 'anaerobicTrainingEffect': None, 'strokes': None, 'normPower': None, 'leftBalance': None, 'rightBalance': None, 'avgLeftBalance': None, 'max20MinPower': None, 'avgVerticalOscillation': None, 'avgGroundContactTime': None, 'avgStrideLength': None, 'avgFractionalCadence': None, 'maxFractionalCadence': None, 'trainingStressScore': None, 'intensityFactor': None, 'vO2MaxValue': None, 'avgVerticalRatio': None, 'avgGroundContactBalance': None, 'lactateThresholdBpm': 158.0, 'lactateThresholdSpeed': None, 'maxFtp': None, 'avgStrokeDistance': None, 'avgStrokeCadence': None, 'maxStrokeCadence': None, 'workoutId': None, 'avgStrokes': None, 'minStrokes': None, 'deviceId': 3907467225, 'minTemperature': 10.0, 'maxTemperature': None, 'minElevation': 2160.0000381469727, 'maxElevation': 5220.000076293945, 'avgDoubleCadence': None, 'maxDoubleCadence': None, 'summarizedExerciseSets': None, 'maxDepth': None, 'avgDepth': None, 'surfaceInterval': None, 'startN2': None, 'endN2': None, 'startCns': None, 'endCns': None, 'summarizedDiveInfo': {'weight': None, 'weightUnit': None, 'visibility': None, 'visibilityUnit': None, 'surfaceCondition': None, 'current': None, 'waterType': None, 'waterDensity': None, 'summarizedDiveGases': [], 'totalSurfaceTime': 0}, 'activityLikeAuthors': None, 'avgVerticalSpeed': None, 'maxVerticalSpeed': 1.1999988555908203, 'floorsClimbed': None, 'floorsDescended': None, 'manufacturer': None, 'diveNumber': None, 'locationName': None, 'bottomTime': None, 'lapCount': 1, 'endLatitude': None, 'endLongitude': None, 'minAirSpeed': None, 'maxAirSpeed': None, 'avgAirSpeed': None, 'avgWindYawAngle': None, 'minCda': None, 'maxCda': None, 'avgCda': None, 'avgWattsPerCda': None, 'flow': None, 'grit': None, 'jumpCount': None, 'caloriesEstimated': None, 'caloriesConsumed': None, 'waterEstimated': None, 'waterConsumed': None, 'maxAvgPower_1': None, 'maxAvgPower_2': None, 'maxAvgPower_5': None, 'maxAvgPower_10': None, 'maxAvgPower_20': None, 'maxAvgPower_30': None, 'maxAvgPower_60': None, 'maxAvgPower_120': None, 'maxAvgPower_300': None, 'maxAvgPower_600': None, 'maxAvgPower_1200': None, 'maxAvgPower_1800': None, 'maxAvgPower_3600': None, 'maxAvgPower_7200': None, 'maxAvgPower_18000': None, 'excludeFromPowerCurveReports': None, 'totalSets': None, 'activeSets': None, 'totalReps': None, 'minRespirationRate': None, 'maxRespirationRate': None, 'avgRespirationRate': None, 'trainingEffectLabel': None, 'activityTrainingLoad': None, 'avgFlow': None, 'avgGrit': None, 'minActivityLapDuration': None, 'startStress': None, 'endStress': None, 'differenceStress': None, 'aerobicTrainingEffectMessage': None, 'anaerobicTrainingEffectMessage': None, 'splitSummaries': [], 'favorite': False, 'pr': False, 'autoCalcCalories': False, 'parent': False, 'atpActivity': False, 'decoDive': None, 'purposeful': False, 'elevationCorrected': False}


'''
Not used:
{
  'startTimeGMT': '2020-03-21 12:16:58',   
  'activityType': {'typeId': 2, 'typeKey': 'cycling', 'parentTypeId': 17, 'sortOrder': 8},
  'eventType': {'typeId': 9, 'typeKey': 'uncategorized', 'sortOrder': 10}, 
  'comments': None, 
  'parentId': None, 
  'elapsedDuration': 8523291.015625, 
  'startLatitude': None, 
  'startLongitude': None,
  'hasPolyline': False, 
  'ownerId': 12331285, 'ownerDisplayName': 'PhaReeseR', 'ownerFullName': 'PhaReeseR', 'ownerProfileImageUrlSmall': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/bc2e1cdc-ae07-40de-821e-3146441104e0-12331285.jpg', 'ownerProfileImageUrlMedium': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/738aef41-8b82-428e-8d48-aff5e9bbf498-12331285.jpg', 'ownerProfileImageUrlLarge': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/3764a7de-8073-46b5-b7be-cd88d7f62cdb-12331285.jpg', 
  'steps': None, 
  'conversationUuid': None, 'conversationPk': None,
  'numberOfActivityLikes': None, 'numberOfActivityComments': None, 'likedByUser': None, 'commentedByUser': None, 'activityLikeDisplayNames': None, 'activityLikeFullNames': None, 
  'requestorRelationship': None, 
  'userRoles': ['ROLE_CONNECTUSER', 'ROLE_FITNESS_USER', 'ROLE_WELLNESS_USER', 'ROLE_OUTDOOR_USER', 'ROLE_CONNECT_2_USER'], 
  'privacy': {'typeId': 2, 'typeKey': 'private'}, 
  'userPro': False, 
  'courseId': None, 
  'hasVideo': False, 'videoUrl': None, 
  'timeZoneId': 124, 
  'beginTimestamp': 1584793018000,
  'sportTypeId': 2, 
  'workoutId': None, 
  'deviceId': 3907467225, 
  'minElevation': 2160.0000381469727, 'maxElevation': 5220.000076293945, 
  'avgDoubleCadence': None, 'maxDoubleCadence': None, 
  'summarizedExerciseSets': None, 
  'maxDepth': None, 'avgDepth': None, 
  'surfaceInterval': None, 
  'startN2': None, 'endN2': None, 'startCns': None, 'endCns': None,
  'summarizedDiveInfo': {'weight': None, 'weightUnit': None, 'visibility': None, 'visibilityUnit': None, 'surfaceCondition': None, 'current': None, 'waterType': None, 'waterDensity': None, 'summarizedDiveGases': [], 'totalSurfaceTime': 0},
  'activityLikeAuthors': None, 
  'avgVerticalSpeed': None, 'maxVerticalSpeed': 1.1999988555908203, 
  'floorsClimbed': None, 'floorsDescended': None, 
  'manufacturer': None, 'diveNumber': None, 
  'locationName': None, 'bottomTime': None, 
  'lapCount': 1, 
  'endLatitude': None, 'endLongitude': None, 
  'minAirSpeed': None, 'maxAirSpeed': None, 'avgAirSpeed': None, 
  'avgWindYawAngle': None, 
  'minCda': None, 'maxCda': None, 'avgCda': None, 'avgWattsPerCda': None, 
  'flow': None, 'grit': None, 'jumpCount': None, 
  'caloriesEstimated': None, 'caloriesConsumed': None, 
  'waterEstimated': None, 'waterConsumed': None, 
  'excludeFromPowerCurveReports': None, 
  'totalSets': None, 'activeSets': None, 
  'totalReps': None, 
  'minRespirationRate': None, 'maxRespirationRate': None, 'avgRespirationRate': None, 
  'trainingEffectLabel': None, 
  'activityTrainingLoad': None, 
  'avgFlow': None, 'avgGrit': None, 
  'minActivityLapDuration': None, 
  'startStress': None, 'endStress': None, 'differenceStress': None, 
  'aerobicTrainingEffectMessage': None, 'anaerobicTrainingEffectMessage': None, 
  'splitSummaries': [], 
  'favorite': False, 
  'pr': False, 
  'autoCalcCalories': False, 
  'parent': False, 
  'atpActivity': False, 
  'decoDive': None, 
  'purposeful': False, 
  'elevationCorrected': False
}
'''

