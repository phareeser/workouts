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
    for data in self.json:
      workouts = json.loads(data)
      for record in workouts:
        workout = Workout()
        workout.source = "JSON import"
        workout.external_id = record['activityId'] 
        sportstype = SportsType(name = record['activityType']['typeKey'])
        workout.sportstype_id = sportstype.add(db)
        workout.sport_id = sportstype.sport_id
        workout.name = record['activityName']
        workout.description = record['description']
        if record['minTemperature']:
          workout.min_temperature = int(record['minTemperature'])
        if record['maxTemperature']:
          workout.max_temperature = int(record['maxTemperature'])
        workout.start_time = datetime.strptime(record['startTimeLocal'], "%Y-%m-%d %H:%M:%S")     # 2020-03-28 16:25:47
        if record['duration']:
          workout.duration_sec = int(record['duration'])
        if record['movingDuration']:
          workout.moving_duration_sec = int(record['movingDuration'])
        if record['distance']:
          workout.distance_m = int(record['distance'])
        if record['averageSpeed']:
          workout.average_speed_m_per_sec = round(record['averageSpeed'], 3)
        if record['maxSpeed']:
          workout.max_speed_m_per_sec = round(record['maxSpeed'], 3)
        workout.elevation_gain_m = record['elevationGain']
        workout.elevation_loss_m = record['elevationLoss']
        workout.calories = record['calories']
        workout.average_hr = record['averageHR']
        workout.max_hr = record['maxHR']
        workout.avg_power = record['avgPower']
        workout.max_power = record['maxPower']
        if record['normPower']:
          workout.norm_power = int(record['normPower'])
        if record['aerobicTrainingEffect']:
          workout.aerobic_training_effect = round(record['aerobicTrainingEffect'], 1)
        if record['anaerobicTrainingEffect']:
          workout.anaerobic_training_effect = round(record['anaerobicTrainingEffect'], 1)
        if record['trainingStressScore']:
          workout.training_stress_score = round(record['trainingStressScore'], 1)
        if record['intensityFactor']:
          workout.intensity_factor = round(record['intensityFactor'], 3)
        if record['averageRunningCadenceInStepsPerMinute']:
          workout.average_running_cadence_steps_per_min = int(record['averageRunningCadenceInStepsPerMinute'])
        if record['maxRunningCadenceInStepsPerMinute']:
          workout.max_running_cadence_steps_per_min = int(record['maxRunningCadenceInStepsPerMinute'])
        workout.average_biking_cadence_rev_per_min = record['averageBikingCadenceInRevPerMinute']
        workout.max_biking_cadence_rev_per_min = record['maxBikingCadenceInRevPerMinute']
        workout.average_swim_cadence_strokes_per_min = record['averageSwimCadenceInStrokesPerMinute']
        workout.max_swim_cadence_strokes_per_min = record['maxSwimCadenceInStrokesPerMinute']
        workout.average_swolf = record['averageSwolf']
        workout.active_lengths = record['activeLengths']
        workout.pool_length = record['poolLength']
        if record['unitOfPoolLength']:
          if record['unitOfPoolLength']['unitKey']:
            workout.unit_of_pool_length = str(record['unitOfPoolLength']['unitKey'])
        if record['unitOfPoolLength']:
          if record['unitOfPoolLength']['factor']:
            workout.pool_length_factor = int(record['unitOfPoolLength']['factor'])
        workout.strokes = record['strokes']
        if record['avgStrokeDistance']:
          workout.avg_stroke_distance = int(record['avgStrokeDistance'])
        workout.avg_stroke_cadence = record['avgStrokeCadence']
        workout.max_stroke_cadence = record['maxStrokeCadence']
        if record['avgStrokes']:
          workout.avg_strokes = round(record['avgStrokes'], 1)
        if record['minStrokes']:
          workout.min_strokes = round(record['minStrokes'], 1)
        workout.left_balance = record['leftBalance']
        workout.right_balance = record['rightBalance']
        workout.avg_left_balance = record['avgLeftBalance']
        if record['avgVerticalOscillation']:
          workout.avg_vertical_oscillation = round(record['avgVerticalOscillation'], 1)
        if record['avgGroundContactTime']:
          workout.avg_ground_contact_time = int(record['avgGroundContactTime'])
        if record['avgStrideLength']:
          workout.avg_stride_length = int(record['avgStrideLength'])
        workout.avg_fractional_cadence = record['avgFractionalCadence']
        workout.max_fractional_cadence = record['maxFractionalCadence']
        if record['avgVerticalRatio']:
          workout.avg_vertical_ratio = round(record['avgVerticalRatio'], 2)
        if record['avgGroundContactBalance']:
          workout.avg_ground_contact_balance = round(record['avgGroundContactBalance'], 2)
        workout.vo2_max_value = record['vO2MaxValue']
        workout.lactate_threshold_bpm = record['lactateThresholdBpm']
        workout.lactate_threshold_speed = record['lactateThresholdSpeed']
        workout.max_ftp = record['maxFtp']
        if record['max20MinPower']:
          workout.max_20_min_power = int(record['max20MinPower'])
        workout.max_avg_power_1 = record['maxAvgPower_1']
        workout.max_avg_power_2 = record['maxAvgPower_2']
        workout.max_avg_power_5 = record['maxAvgPower_5']
        workout.max_avg_power_10 = record['maxAvgPower_10']
        workout.max_avg_power_20 = record['maxAvgPower_20']
        workout.max_avg_power_30 = record['maxAvgPower_30']          
        workout.max_avg_power_60 = record['maxAvgPower_60']
        workout.max_avg_power_120 = record['maxAvgPower_120']
        workout.max_avg_power_300 = record['maxAvgPower_300']
        workout.max_avg_power_600 = record['maxAvgPower_600']
        workout.max_avg_power_1200 = record['maxAvgPower_1200']
        workout.max_avg_power_1800 = record['maxAvgPower_1800']
        workout.max_avg_power_3600 = record['maxAvgPower_3600']
        workout.max_avg_power_7200 = record['maxAvgPower_7200']
        workout.max_avg_power_18000 = record['maxAvgPower_18000']
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

