from datetime import datetime, date
from pydantic import BaseModel, computed_field, ConfigDict, Field, AliasChoices


class LaunchTargetSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str
    name: str
    details: str | None
    rocket_id: str = Field(validation_alias=AliasChoices('rocket', 'rocket_id'))
    rocket_name: str
    flight_number: int
    success: bool | None

    launch_date_utc: datetime = Field(validation_alias=AliasChoices("date_utc", 'launch_date_utc'))
    launch_date_local: datetime = Field(validation_alias=AliasChoices("date_local", 'launch_date_local'))
    launch_date_precision: str = Field(validation_alias=AliasChoices("date_precision", 'launch_date_precision'))
    launch_date_unix: int = Field(validation_alias=AliasChoices("date_unix", 'launch_date_unix'))

    @computed_field
    def transformed_at_utc(self) -> datetime:
        return datetime.now()

    @computed_field
    def transformed_at_date(self) -> date:
        return datetime.now().date()


class LaunchTargetSchemaList(BaseModel):
    launches: list[LaunchTargetSchema | None]
