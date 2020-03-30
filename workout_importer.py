"""
Abstract base class for importing workouts
"""

import abc
import logging

class WorkoutImporter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, log_level):
      if log_level:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
      else:
        logging.basicConfig(format="%(levelname)s: %(message)s")
      self.log = logging
  
    @abc.abstractmethod
    def create_session(self):
      pass
  
    @abc.abstractmethod
    def close_session(self):
      pass
  
    @abc.abstractmethod
    def import_workouts(self):
      pass
  
