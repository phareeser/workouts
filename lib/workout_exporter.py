import abc


class WorkoutExporter(metaclass=abc.ABCMeta):
    """
    Abstract base class for exporting workouts
    """
    
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
    def export_workouts(self):
        pass
