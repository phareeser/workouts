'''
Test Cases for importing workouts in CSV format
- happy paths
    - number of imported workouts is correct
    - already existing workouts are identified and not imported
    - duplicate workouts are identified and marked
- unhappy paths
    - import file has wrong format
    - workouts have incorrect syntax 
'''

import unittest
import os

import lib
from lib.csv_importer import CsvImporter
from lib.workout import WorkoutsDatabase, Workout


class TestImportCSV(unittest.TestCase):

    def setUp(self):
        self.db = WorkoutsDatabase("testdb")
        self.db.create_session()
        self.csv = CsvImporter(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./sample.csv"))
        self.csv.create_session()

    def tearDown(self):
        self.csv.close_session()
        self.db.close_session()
        os.remove("testdb")

    def test_import(self):
        number_of_workouts = self.db.session.query(Workout.id).count()
        (fetched, imported) = self.csv.import_workouts(self.db)
        # 3 more workouts in db?
        self.assertEqual(number_of_workouts+3,
                    self.db.session.query(Workout.id).count())
        # from 3 imported workouts 3 are new
        self.assertEqual((fetched, imported), (3, 3))
        # workout imported with correct attribues
        workout = self.db.session.query(Workout).filter(Workout.external_id == 42).first()
        self.assertEqual(workout.name, "Indoor Rad")

    def test_import_existing(self):
        self.csv.import_workouts(self.db)
        number_of_workouts = self.db.session.query(Workout.id).count()
        # 2nd import of the same workouts
        self.csv.csv.seek(0) # reset file pointer
        (fetched, imported) = self.csv.import_workouts(self.db)
        # no more workouts in db?
        self.assertEqual(number_of_workouts,
                         self.db.session.query(Workout.id).count())
        # from 2 imported workouts 0 are new
        self.assertEqual((fetched, imported), (3, 0))



        
