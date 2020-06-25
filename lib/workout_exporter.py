import abc


class WorkoutExporter(metaclass=abc.ABCMeta):
    """
    Abstract base class for exporting workouts
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
    def export_workouts(self):
        raise NotImplementedError
