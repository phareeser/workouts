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
        sport = Sport()
        sport.name = "TEST_SPORT"
        sport.add(self.db)
        self.assertEqual(number_of_sports + 1,
                         self.db.session.query(Sport.id).count())
        self.assertEqual("TEST_SPORT", self.db.session.query(
            Sport.name).filter(Sport.id == sport.id).first()[0])

    def test_get_sport(self):
        sport = Sport()
        sport.name = "TEST_SPORT"
        sport.add(self.db)
        self.assertTrue("TEST_SPORT" in str(Sport.get(self.db, "TEST_SPORT")))
        self.assertIsNone(Sport.get(self.db, "blablubb"))


class TestSportsType(unittest.TestCase):
    DB_NAME = "test.db"

    def setUp(self):
        self.db = WorkoutsDatabase(self.DB_NAME)

    def tearDown(self):
        self.db.close()
        os.remove(self.DB_NAME)

    def test_add_sportstype(self):
        number_of_sportstypes = self.db.session.query(SportsType.id).count()
        sportstype = SportsType()
        sportstype.name = "TEST_SPORTSTYPE"
        sportstype.add(self.db)
        self.assertEqual(number_of_sportstypes + 1,
                         self.db.session.query(SportsType.id).count())
        self.assertEqual("TEST_SPORTSTYPE", self.db.session.query(
            SportsType.name).filter(SportsType.id == sportstype.id).first()[0])

    def test_get_sport(self):
        sportstype = SportsType()
        sportstype.name = "TEST_SPORTSTYPE"
        sportstype.add(self.db)
        self.assertTrue("TEST_SPORTSTYPE" in str(
            SportsType.get(self.db, "TEST_SPORTSTYPE")))
        self.assertIsNone(SportsType.get(self.db, "blablubb"))

    def test_associate_sport(self):
        sportstype = SportsType()
        sportstype.name = "Indoor Cycling"
        sportstype.associate_sport(self.db)
        self.assertEqual(sportstype.sport_id, self.db.session.query(Sport.id).filter(Sport.name == "Cycling").first()[0])
        sportstype.name = "New Type"
        sportstype.associate_sport(self.db)
        self.assertEqual(sportstype.sport_id, self.db.session.query(Sport.id).filter(Sport.name == "New Type").first()[0])

    def test_cleanup_sportstype(self):
        sportstype = SportsType()
        sportstype.name = "RuNnInG"
        sportstype.cleanup_sportstype()
        self.assertEqual(sportstype.name, "Running")


if __name__ == '__main__':
    unittest.main()
