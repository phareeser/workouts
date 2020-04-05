"""
Abstract base class for importing workouts
"""

import abc

class WorkoutImporter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
      pass
  
    @abc.abstractmethod
    def create_session(self):
      pass
  
    @abc.abstractmethod
    def close_session(self):
      pass
  
    @abc.abstractmethod
    def import_workouts(self):
      pass
  
