import abc


class WorkoutImporter(metaclass=abc.ABCMeta):
    """
    Abstract base class for importing workouts
    """

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError


    @abc.abstractmethod
    def create_session(self):
        raise NotImplementedError

    @abc.abstractmethod
    def close_session(self):
        raise NotImplementedError

    @abc.abstractmethod
    def import_workouts(self):
        raise NotImplementedError
