import unittest
import os
from datetime import datetime

import lib
from lib.workout import Workout, WorkoutsDatabase, Sport, SportsType

class TestDuplicateWorkouts(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        self.db = WorkoutsDatabase(self.DB_NAME)

    def tearDown(self):
        self.db.close()
        os.remove(self.DB_NAME)

    def test_duplicate_workouts(self):
        # this workout                          |-----------------|
        # 1st potential duplicate in db     |-----------------|
        # 2nd potential duplicate in db     |------------------------|
        # 3rd potential duplicate in db             |----------------|
        # 4th potential duplicate in db             |---------|

        number_of_workouts_before = self.db.session.query(Workout.id).count()
        id_counter = 0
        workout = Workout(external_id=id_counter,
                          sportstype_id=1,
                          sport_id=1,
                          start_time=datetime.strptime("2020-05-21 20:00:00", "%Y-%m-%d %H:%M:%S"),
                          duration_sec=600)
        workout.add(self.db)
        number_of_workouts_after = self.db.session.query(Workout.id).count()
        self.assertTrue(number_of_workouts_after == number_of_workouts_before + 1)

        # time is overlapping, same sport -> is_duplicate
        number_of_workouts_before = number_of_workouts_after
        id_counter += 1
        workout = Workout(external_id=id_counter,
                          sportstype_id=1,
                          sport_id=1,
                          start_time=datetime.strptime(
                              "2020-05-21 19:58:00", "%Y-%m-%d %H:%M:%S"),
                          duration_sec=600)
        workout.add(self.db)
        number_of_workouts_after = self.db.session.query(Workout.id).count()
        self.assertTrue(number_of_workouts_after ==
                        number_of_workouts_before + 1)
        #self.assertIsNotNone(workout.is_duplicate_with)

        # time is overlapping, same sport -> is_duplicate
        number_of_workouts_before = number_of_workouts_after
        id_counter += 1
        workout = Workout(external_id=id_counter,
                          sportstype_id=1,
                          sport_id=1,
                          start_time=datetime.strptime("2020-05-21 20:02:00", "%Y-%m-%d %H:%M:%S"),
                          duration_sec=600)
        workout.add(self.db)
        number_of_workouts_after = self.db.session.query(Workout.id).count()
        self.assertTrue(number_of_workouts_after == number_of_workouts_before + 1)
        #self.assertIsNotNone(workout.is_duplicate_with)

        # time is overlapping, different sport -> manual_check_required_with
        number_of_workouts_before = number_of_workouts_after
        id_counter += 1
        workout = Workout(external_id=id_counter,
                          sportstype_id=2,
                          sport_id=2,
                          start_time=datetime.strptime("2020-05-21 20:01:00", "%Y-%m-%d %H:%M:%S"),
                          duration_sec=600)
        workout.add(self.db)
        number_of_workouts_after = self.db.session.query(Workout.id).count()
        self.assertTrue(number_of_workouts_after == number_of_workouts_before + 1)
        self.assertIsNotNone(workout.manual_check_required_with)

        # time not overlapping, no duplicate
        number_of_workouts_before = number_of_workouts_after
        id_counter += 1
        workout = Workout(external_id=id_counter,
                          sportstype_id=1,
                          sport_id=1,
                          start_time=datetime.strptime("2020-05-22 20:11:00", "%Y-%m-%d %H:%M:%S"),
                          duration_sec=600)
        workout.add(self.db)
        number_of_workouts_after = self.db.session.query(Workout.id).count()
        self.assertTrue(number_of_workouts_after == number_of_workouts_before + 1)
        self.assertIsNone(workout.is_duplicate_with)

if __name__ == '__main__':
    unittest.main()
