import unittest
import os

import lib
from lib.csv_importer import CsvImporter
from lib.workout import WorkoutsDatabase, Workout


class TestImportCSV(unittest.TestCase):

    def setUp(self):
        self.db = WorkoutsDatabase("testdb")
        self.csv = CsvImporter(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./sample.csv"))
        self.csv.create_session()

    def tearDown(self):
        self.csv.close_session()
        self.db.close()
        os.remove("testdb")

    def test_import(self):
        number_of_workouts = self.db.session.query(Workout.id).count()
        val = self.csv.import_workouts(self.db)
        self.assertEqual(number_of_workouts+2,
                    self.db.session.query(Workout.id).count())
        self.assertEqual(val, (2, 2))

        workout = self.db.session.query(Workout).filter(Workout.external_id == 42).first()
        self.assertEqual(workout.name, "Indoor Rad")



        
