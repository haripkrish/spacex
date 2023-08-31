import abc
from enum import Enum, auto
from src.core.data_pipeline.task import Task


class PipelineStage(Enum):
    RAW: str = 'raw'
    VALIDATED: str = 'validated'
    INTERMEDIATE: str = 'intermediate'
    ERRORED: str = 'errored'


class DataPipeline(abc.ABC):
    class Extraction(Task):

        @abc.abstractmethod
        def partial_extract(self):
            pass

        @abc.abstractmethod
        def full_extract(self):
            pass

    class Validation(Task):

        @abc.abstractmethod
        def validate(self):
            pass

    class Transformation(Task):

        @abc.abstractmethod
        def transform(self):
            pass

    class Load(Task):

        @abc.abstractmethod
        def load(self):
            pass
