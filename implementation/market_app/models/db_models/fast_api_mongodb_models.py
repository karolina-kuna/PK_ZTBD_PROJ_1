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


class OfferAddressModel(BaseModel):
    id: PyObjectId
    city: str
    street: str


class OfferOwnerModel(BaseModel):
    id: PyObjectId
    company_name: str


class OfferModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    address: Dict[str, Any] = Field(...)
    price: float = Field(..., gt=0.0)
    title: str = Field(...)
    area: float = Field(..., gt=0.0)
    owner: Dict[str, Any] = Field(...)
    apartment_id: int = Field(..., gt=0)

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


class Owner:
    def __init__(self, surname: str, phone_number: str, address: str, email_address: str,
                 company_name: str, _id=None):
        if _id is not None:
            self._id = _id

        self.surname = surname
        self.phone_number = phone_number
        self.address = address
        self.email_address = email_address
        self.company_name = company_name

    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None

class OwnerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    surname: str = Field(...)
    phone_number: str = Field(...)
    address: str = Field(...)
    email_address: str = Field(...)
    company_name: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
