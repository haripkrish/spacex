import abc


class Task(abc.ABC):

    @abc.abstractmethod
    def dependency(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass
