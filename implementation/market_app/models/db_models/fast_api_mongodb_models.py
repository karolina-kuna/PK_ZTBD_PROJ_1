import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List, Dict, Any


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class OfferAddressModel:
    id: str
    city: str
    street: str


class OfferOwnerModel:
    id: str
    company_name: str




class OfferModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    address: Dict[str, Any] = Field(...)
    price: float = Field(..., gt=0.0)
    title: str = Field(...)
    status: str = Field(...)
    description: str = Field(...)
    agency_fee: float = Field(...)
    negotiable: bool = Field(...)
    creation_date: datetime.datetime = Field(...)
    modification_date: datetime.datetime = Field(...)
    area: float = Field(..., gt=0.0)
    owner: Dict[str, Any] = Field(...)
    apartment_id: PyObjectId = Field(default_factory=PyObjectId)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "address": {
                    "_id": "5f1d24e9c53b1a7d5c345678",
                    "city": "New York",
                    "street": "123 Main St",
                },
                "price": 500000.0,
                "title": "Luxury apartment in the heart of the city",
                "area": 120.0,
                "owner": {
                    "_id": "5f1d25a9c53b1a7d5c345679",
                    "company_name": "Acme Real Estate",
                },
                "apartment_id": 123,
                "company_name": "Acme Real Estate",
            }
        }


class AddressModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    city: str = Field(...)
    street_name: str = Field(...)
    building_nr: str = Field(...)
    apartment_nr: str = Field(...)
    postal_code: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "city": "New York",
                "street_name": "Main St",
                "building_nr": "123",
                "apartment_nr": "4B",
                "postal_code": "10001"
            }
        }


class OwnerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    surname: str = Field(...)
    phone_number: str = Field(...)
    address: str = Field(...)
    email_address: str = Field(...)
    company_name: Optional[str] = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ApartmentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    area: float = Field(...)
    creation_year: int = Field(...)
    last_renovation_year: int = Field(...)
    building_type: str = Field(...)
    heating_type: str = Field(...)
    is_furnished: bool = Field(...)
    rooms_count: int = Field(...)
    owner_id: PyObjectId = Field(default_factory=PyObjectId)
    address_id: PyObjectId = Field(default_factory=PyObjectId)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
