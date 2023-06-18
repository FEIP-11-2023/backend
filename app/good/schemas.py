import decimal
import re
import uuid
from typing import Optional

from app.good import models
from app.good import exceptions
from app.models import ORJSONModel
from pydantic import validator


class CreateBrand(ORJSONModel):
    name: str


class UpdateBrand(CreateBrand):
    brand_id: uuid.UUID


class CreateColor(ORJSONModel):
    name: str


class UpdateColor(CreateColor):
    color_id: uuid.UUID


class CreateCategory(ORJSONModel):
    name: str


class UpdateCategory(CreateCategory):
    category_id: uuid.UUID


class CreateGood(ORJSONModel):
    name: str
    description: str
    price: decimal.Decimal
    category_id: uuid.UUID
    color_id: uuid.UUID
    brand_id: uuid.UUID


class AddGoodSize(ORJSONModel):
    good_id: uuid.UUID
    size: int
    remainder: int


class SetGoodRemainder(ORJSONModel):
    size_id: uuid.UUID
    remainder: int

    @validator("remainder")
    def validate_password(cls, remainder, **kwargs):
        if remainder < 0:
            raise exceptions.RemainderCannotBeNegative
        return remainder


class AddToGoodRemainder(ORJSONModel):
    size_id: uuid.UUID
    delta: int

    @validator("delta")
    def validate_password(cls, delta, **kwargs):
        if delta < 0:
            raise exceptions.DeltaCannotBeNegative
        return delta


class UpdateGood(CreateGood):
    good_id: uuid.UUID


class CreateSale(ORJSONModel):
    good_id: uuid.UUID
    size: int
    active: bool


class SwitchSale(ORJSONModel):
    sale_id: uuid.UUID
    active: bool
