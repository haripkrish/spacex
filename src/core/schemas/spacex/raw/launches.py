from typing import List, Optional
from pydantic import BaseModel


class Fairings(BaseModel):
    reused: Optional[bool]
    recovery_attempt: Optional[bool]
    recovered: Optional[bool]
    ships: List[str | None]


class Patch(BaseModel):
    small: Optional[str]
    large: Optional[str]


class RedditLinks(BaseModel):
    campaign: Optional[str]
    launch: Optional[str]
    media: Optional[str]
    recovery: Optional[str]


class FlickrLinks(BaseModel):
    small: Optional[List[str]]
    original: Optional[List[str]]


class Links(BaseModel):
    patch: Optional[Patch]
    reddit: Optional[RedditLinks]
    flickr: Optional[FlickrLinks]
    presskit: Optional[str]
    webcast: Optional[str]
    youtube_id: Optional[str]
    article: Optional[str]
    wikipedia: Optional[str]


class crew(BaseModel):
    crew: Optional[str]
    role: Optional[str]


class Failure(BaseModel):
    time: int
    altitude: Optional[int]
    reason: str


class Core(BaseModel):
    core: Optional[str]
    flight: Optional[int]
    gridfins: Optional[bool]
    legs: Optional[bool]
    reused: Optional[bool]
    landing_attempt: Optional[bool]
    landing_success: Optional[bool]
    landing_type: Optional[str]
    landpad: Optional[str]


class Payload(BaseModel):
    payload: str


class Launch(BaseModel):
    fairings: Optional[Fairings | None]
    links: Optional[Links | None]
    static_fire_date_utc: Optional[str]
    static_fire_date_unix: Optional[int]
    net: bool | None
    window: int | None
    rocket: str | None
    success: bool | None
    failures: List[Failure]
    details: Optional[str]
    crew: List[crew | None]
    ships: List[str | None]
    capsules: List[str]
    payloads: List[str]
    launchpad: str
    flight_number: int
    name: str
    date_utc: str
    date_unix: int
    date_local: str
    date_precision: str
    upcoming: bool
    cores: List[Core]
    auto_update: bool
    tbd: bool
    launch_library_id: Optional[str]
    id: str


class LaunchList(Launch):
    launches: List[Launch]
