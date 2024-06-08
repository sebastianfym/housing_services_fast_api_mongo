# from pydantic import BaseModel, Field
# from typing import Optional, List
# from bson import ObjectId
# from datetime import datetime
#
#
# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v, values, **kwargs):
#         if not ObjectId.is_valid(v):
#             raise ValueError('Invalid objectid')
#         return ObjectId(v)
#
#     @classmethod
#     def __get_pydantic_json_schema__(cls, core_schema, handler):
#         json_schema = handler(core_schema)
#         json_schema.update(type='string')
#         return json_schema
#
#
# class Tariff(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
#     name: str
#     rate: float  # Price per unit
#     unit: str  # Unit of the resource (e.g., cubic meter for water)
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class WaterMeterReading(BaseModel):
#     date: datetime = Field(default_factory=datetime.now)
#     value: float  # Meter reading value
#
#
# class WaterMeter(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
#     readings: List[WaterMeterReading] = []
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class Apartment(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
#     number: int
#     area: float  # Area in square meters
#     water_meters: List[WaterMeter] = []
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class House(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
#     address: str
#     apartments: List[Apartment] = []
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class RentCalculationRequest(BaseModel):
#     month: int
#     year: int
#
#
# class MonthlyCharge(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
#     house_id: str
#     apartment_id: str
#     month: int
#     year: int
#     total_water_charge: float
#     maintenance_charge: float
#     total_charge: float
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}

from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type='string')
        return json_schema


class Tariff(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    rate: float  # Price per unit
    unit: str  # Unit of the resource (e.g., cubic meter for water)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class WaterMeterReading(BaseModel):
    date: datetime = Field(default_factory=datetime.now)
    value: float  # Meter reading value


class WaterMeter(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    readings: List[WaterMeterReading] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Apartment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    number: int
    area: float  # Area in square meters
    water_meters: List[WaterMeter] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class House(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    address: str
    apartments: List[Apartment] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RentCalculationRequest(BaseModel):
    month: int
    year: int


class MonthlyCharge(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    house_id: str
    apartment_id: str
    month: int
    year: int
    total_water_charge: float
    maintenance_charge: float
    total_charge: float
    status: str = "completed"

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
