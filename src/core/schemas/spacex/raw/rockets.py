from pydantic import BaseModel
from typing import List, Optional


class Dimensions(BaseModel):
    meters: Optional[float]
    feet: Optional[float]


class Mass(BaseModel):
    kg: Optional[int]
    lb: Optional[int]


class Thrust(BaseModel):
    kN: Optional[int]
    lbf: Optional[int]


class FirstStage(BaseModel):
    thrust_sea_level: Optional[Thrust]
    thrust_vacuum: Optional[Thrust]
    reusable: Optional[bool]
    engines: Optional[int]
    fuel_amount_tons: Optional[float]
    burn_time_sec: Optional[int]


class CompositeFairing(BaseModel):
    height: Optional[Dimensions]
    diameter: Optional[Dimensions]


class SecondStage(BaseModel):
    thrust: Optional[Thrust]
    payloads: Optional[dict]
    reusable: Optional[bool]
    engines: Optional[int]
    fuel_amount_tons: Optional[float]
    burn_time_sec: Optional[int]


class Engines(BaseModel):
    isp: Optional[dict]
    thrust_sea_level: Optional[Thrust]
    thrust_vacuum: Optional[Thrust]
    number: Optional[int]
    type: Optional[str]
    version: Optional[str]
    layout: Optional[str]
    engine_loss_max: Optional[int]
    propellant_1: Optional[str]
    propellant_2: Optional[str]
    thrust_to_weight: Optional[float]


class LandingLegs(BaseModel):
    number: Optional[int]
    material: Optional[str]


class PayloadWeight(BaseModel):
    id: Optional[str]
    name: Optional[str]
    kg: Optional[int]
    lb: Optional[int]


class Rocket(BaseModel):
    height: Optional[Dimensions]
    diameter: Optional[Dimensions]
    mass: Optional[Mass]
    first_stage: Optional[FirstStage]
    second_stage: Optional[SecondStage]
    engines: Optional[Engines]
    landing_legs: Optional[LandingLegs]
    payload_weights: Optional[List[PayloadWeight]]
    flickr_images: Optional[List[str]]
    name: Optional[str]
    type: Optional[str]
    active: Optional[bool]
    stages: Optional[int]
    boosters: Optional[int]
    cost_per_launch: Optional[int]
    success_rate_pct: Optional[int]
    first_flight: Optional[str]
    country: Optional[str]
    company: Optional[str]
    wikipedia: Optional[str]
    description: Optional[str]
    id: str
