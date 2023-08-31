import os
import json
from datetime import datetime
from src.logs.config import logger

from src.config.config import settings
from src.core.data_pipeline.data_pipeline import DataPipeline, PipelineStage
from src.core.schemas.spacex.raw.launches import Launch
from src.core.schemas.spacex.raw.rockets import Rocket
from src.core.schemas.spacex.target.launches import LaunchTargetSchema, LaunchTargetSchemaList
from src.core.spacex_api.spacex_api_client import SpaceXAPIClient
from src.db.asyncpg_db import PGDatabase, bulk_upsert_postgres


class DataPipelineHelper:
    def create_folder(self, file_path, folder_name):
        folder_name = f"{file_path}/{folder_name}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def write_json_file_by_date(self, file_path, file_name, data):
        new_filename = f"{file_path}/{file_name}.json"
        with open(new_filename, 'w') as f:
            f.write(data)

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            return f.read()

    def load_json_file(self, file_path):
        return json.loads(self.read_file(file_path))

    def pre_task_exec(self, pipeline_name, location):
        folder_path = self.create_folder(f"{location}", pipeline_name)
        batch_run_folder_path = self.create_folder(folder_path, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        stage_folders = {
            stage.value: self.create_folder(batch_run_folder_path, stage.value)
            for stage in PipelineStage
        }
        return stage_folders


class SpacexAPIDataPipeline(DataPipeline, DataPipelineHelper):

    def __init__(self):
        self.pipeline_name = 'spacex_api_data_pipeline'
        self.pipeline_description = 'This is a data pipeline for the SpaceX API'
        self.endpoints = ['launches', 'rockets']
        self.task_dependency = {
            'extract': False,
            'validate': False,
            'transform': False,
            'load': False
        }
        self.extraction = self.Extraction(self)
        self.validation = self.Validation(self)
        self.transformation = self.Transformation(self)
        self.load = self.Load(self)
        self.stage_folders = self.pre_task_exec(self.pipeline_name, 'data')

    class Extraction(DataPipeline.Extraction):

        def __init__(self, dag_level_attributes):
            super().__init__()
            self.dag_level_attributes = dag_level_attributes
            self.api_client = SpaceXAPIClient()

        def full_extract(self):
            for endpoint in self.dag_level_attributes.endpoints:
                data = self.api_client.fetch_data_by_endpoint(endpoint)
                file_path = self.dag_level_attributes.stage_folders[PipelineStage.RAW.value]
                self.dag_level_attributes.write_json_file_by_date(file_path, endpoint, json.dumps(data))

        def partial_extract(self):
            pass

        def dependency(self):
            return True

        def run(self):
            try:
                logger.info(f"Running {self.__class__.__name__}")
                self.full_extract()
                self.dag_level_attributes.task_dependency['extract'] = True
                logger.info("Saved the extracted data to the raw folder")
                logger.info(f"Completed {self.__class__.__name__}")
            except Exception as e:
                logger.error(f"Extraction failed: {e}")

    class Validation(DataPipeline.Validation):

        def __init__(self, dag_level_attributes):
            super().__init__()
            self.dag_level_attributes = dag_level_attributes
            self.endpoint_validation_mapping = {
                'launches': Launch,
                'rockets': Rocket
            }

        def validate(self):
            for endpoint in self.dag_level_attributes.endpoints:
                data = self.dag_level_attributes.load_json_file(
                    f"{self.dag_level_attributes.stage_folders[PipelineStage.RAW.value]}/{endpoint}.json")
                validation = {
                    'success': [],
                    'failure': []
                }
                for record in data:
                    try:
                        self.endpoint_validation_mapping[endpoint](**record)
                        validation.get('success').append(record)
                    except Exception as e:
                        validation.get('failure').append(record)
                        logger.error(f"Validation failed: {e}")
                for k, v in validation.items():
                    if k == 'success':
                        file_path = self.dag_level_attributes.stage_folders[
                            PipelineStage.VALIDATED.value]
                    else:
                        file_path = self.dag_level_attributes.stage_folders[PipelineStage.ERRORED.value]
                    self.dag_level_attributes.write_json_file_by_date(file_path, endpoint, json.dumps(v))

        def dependency(self):
            return self.dag_level_attributes.task_dependency.get('extract')

        def run(self):
            if self.dependency():
                try:
                    logger.info(f"Running {self.__class__.__name__}")
                    self.validate()
                    self.dag_level_attributes.task_dependency['validate'] = True
                    logger.info("Saved the validated data to the validated and errored folders")
                    logger.info(f"Completed {self.__class__.__name__}")
                except Exception as e:
                    logger.error(f"Validation failed: {e}")
            else:
                logger.info("Dependency failed")

    class Transformation(DataPipeline.Transformation):

        def __init__(self, dag_level_attributes):
            super().__init__()
            self.dag_level_attributes = dag_level_attributes

        def launch_transform(self, endpoint='launches'):
            # load validated data of launches and rockets
            launches = self.dag_level_attributes.load_json_file(
                f"{self.dag_level_attributes.stage_folders[PipelineStage.VALIDATED.value]}/launches.json")
            rockets = self.dag_level_attributes.load_json_file(
                f"{self.dag_level_attributes.stage_folders[PipelineStage.VALIDATED.value]}/rockets.json")
            # create a dict of rocket id and rocket name
            rocket_id_name_mapping = {rocket.get('id'): rocket.get('name') for rocket in rockets}

            # transform launches data
            transformed_result = []
            for launch in launches:
                rocket_name = rocket_id_name_mapping.get(launch.get('rocket'))
                launch_target = LaunchTargetSchema(**launch, rocket_name=rocket_name)
                transformed_result.append(launch_target)
            LaunchTargetSchemaList(launches=transformed_result).model_dump_json()

            # write transformed data to intermediate folder
            file_path = self.dag_level_attributes.stage_folders[PipelineStage.INTERMEDIATE.value]
            self.dag_level_attributes.write_json_file_by_date(file_path, endpoint, LaunchTargetSchemaList(
                launches=transformed_result).model_dump_json())

        def transform(self):
            self.launch_transform()

        def dependency(self):
            return self.dag_level_attributes.task_dependency.get('validate')

        def run(self):
            if self.dependency():
                try:
                    logger.info(f"Running {self.__class__.__name__}")
                    self.transform()
                    self.dag_level_attributes.task_dependency['transform'] = True
                    logger.info("Saved the transformed data to the intermediate folder")
                    logger.info(f"Completed {self.__class__.__name__}")
                except Exception as e:
                    logger.error(f"Transformation failed: {e} ")
            else:
                logger.info("Dependency failed ")

    class Load(DataPipeline.Load):

        def __init__(self, task_level_attributes):
            super().__init__()
            self.task_level_attributes = task_level_attributes

        def get_db(self):
            return PGDatabase(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                database=settings.POSTGRES_DB,
                host=settings.POSTGRES_HOST
            )

        def load(self):
            # load transformed data of launches from intermediate folder
            file_data_obj = self.task_level_attributes.load_json_file(
                f"{self.task_level_attributes.stage_folders[PipelineStage.INTERMEDIATE.value]}/launches.json")
            # upsert transformed data of launches to postgres
            db = self.get_db()
            launches_values, launches_fields = [], ()
            for record in file_data_obj.get('launches'):
                validated_record = LaunchTargetSchema(**record)
                validated_record_dict = validated_record.model_dump()
                launches_values.append(tuple(validated_record_dict.values()))
                launches_fields = validated_record_dict.keys()
            bulk_upsert_postgres(db, 'launches', launches_fields, launches_values)

        def dependency(self):
            return self.task_level_attributes.task_dependency.get('transform')

        def run(self):
            if self.dependency():
                try:
                    logger.info(f"Running {self.__class__.__name__}")
                    self.load()
                    self.task_level_attributes.task_dependency['load'] = True
                    logger.info("Loaded the transformed data to the postgres db")
                    logger.info(f"Completed {self.__class__.__name__} ")
                except Exception as e:
                    logger.error(f"Load failed: {e} ")
            else:
                logger.info("Dependency failed")

    def main(self):
        self.extraction.run()
        self.validation.run()
        self.transformation.run()
        self.load.run()
        logger.info(f"Pipeline {self.pipeline_name} with task status as {self.task_dependency}")
