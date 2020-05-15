import unittest
import os

import lib
from lib.workout import Workout, WorkoutsDatabase, Sport, SportsType

class TestWorkoutsDatabase(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_session(self):
        db = WorkoutsDatabase(self.DB_NAME)
        self.assertIsNotNone(db)
        os.remove(self.DB_NAME)


class TestSport(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        self.db = WorkoutsDatabase(self.DB_NAME)

    def tearDown(self):
        self.db.close()
        os.remove(self.DB_NAME)

    def test_add_sport(self):
        number_of_sports = self.db.session.query(Sport.id).count()
        sport = Sport(name = "TEST_SPORT")
        sport.add(self.db)
        self.assertEqual(number_of_sports + 1,
                         self.db.session.query(Sport.id).count())
        self.assertEqual("TEST_SPORT", self.db.session.query(
            Sport.name).filter(Sport.id == sport.id).first()[0])


class TestSportsType(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        self.db = WorkoutsDatabase(self.DB_NAME)

    def tearDown(self):
        self.db.close()
        os.remove(self.DB_NAME)

    def test_add_sportstype(self):
        number_of_sportstypes = self.db.session.query(SportsType.id).count()
        sportstype = SportsType(name = "TEST_SPORTSTYPE")
        sportstype.add(self.db)
        self.assertEqual(number_of_sportstypes + 1,
                         self.db.session.query(SportsType.id).count())
        self.assertEqual("TEST_SPORTSTYPE", self.db.session.query(
            SportsType.name).filter(SportsType.id == sportstype.id).first()[0])

    def test_associate_sport(self):
        sportstype = SportsType(name = "Indoor Cycling")
        sportstype.associate_sport(self.db)
        self.assertEqual(sportstype.sport_id, self.db.session.query(Sport.id).filter(Sport.name == "Cycling").first()[0])
        sportstype.name = "New Type"
        sportstype.associate_sport(self.db)
        self.assertEqual(sportstype.sport_id, self.db.session.query(Sport.id).filter(Sport.name == "New Type").first()[0])

    def test_cleanup_sportstype(self):
        sportstype = SportsType(name = "RuNnInG")
        sportstype.cleanup_sportstype()
        self.assertEqual(sportstype.name, "Running")


class TestWorkout(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        self.db = WorkoutsDatabase(self.DB_NAME)

    def tearDown(self):
        self.db.close()
        os.remove(self.DB_NAME)

    def test_add_workout(self):
        number_of_workouts = self.db.session.query(Workout.id).count()
        workout = Workout(name="TEST_WORKOUT")
        workout.add(self.db)
        self.assertEqual(number_of_workouts + 1,
                         self.db.session.query(Workout.id).count())
        self.assertEqual("TEST_WORKOUT", self.db.session.query(
            Workout.name).filter(Workout.id == workout.id).first()[0])

    def test_workout_as_dict(self):
        workout = Workout(name = "TEST_WORKOUT")
        sportstype = SportsType(name = "TEST_SPORTSTYPE")
        sportstype.add(self.db)
        workout.sportstype_id = sportstype.id
        workout.sport_id = sportstype.sport_id
        workout.add(self.db)

        as_dict = workout.as_dict(self.db)
        self.assertTrue(isinstance(as_dict, dict))
        self.assertIn('id', as_dict)
        self.assertNotIn('external_id', as_dict)
        self.assertIn('name', as_dict)
        self.assertNotIn('sportstype_id', as_dict)
        self.assertIn('sportstype', as_dict)

    def test_workout_as_list(self):
        workout = Workout(name="TEST_WORKOUT")
        sportstype = SportsType(name="TEST_SPORTSTYPE")
        sportstype.add(self.db)
        workout.sportstype_id = sportstype.id
        workout.sport_id = sportstype.sport_id
        workout.add(self.db)

        as_list = workout.as_list(self.db)
        self.assertTrue(isinstance(as_list, list))
        self.assertIn('TEST_WORKOUT', as_list)
        self.assertIn('TEST_SPORTSTYPE', as_list)


if __name__ == '__main__':
    unittest.main()
