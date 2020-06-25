import unittest
import os

import lib
from lib.json_importer import JsonImporter
from lib.workout import WorkoutsDatabase, Workout


class TestImportCSV(unittest.TestCase):

    def setUp(self):
        self.db = WorkoutsDatabase("testdb")
        self.db.create_session()
        self.json = JsonImporter(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "./sample.json"))
        self.json.create_session()

    def tearDown(self):
        self.json.close_session()
        self.db.close_session()
        os.remove("testdb")

    def test_import(self):
        number_of_workouts = self.db.session.query(Workout.id).count()
        val = self.json.import_workouts(self.db)
        self.assertEqual(number_of_workouts+2,
                         self.db.session.query(Workout.id).count())
        self.assertEqual(val, (2, 2))

        workout = self.db.session.query(Workout).filter(
            Workout.external_id == 42).first()
        self.assertEqual(workout.name, "Indoor Rad")
