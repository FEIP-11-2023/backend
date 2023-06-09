import decimal
import uuid
from typing import List, Optional

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


class Color(ORJSONModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class Brand(ORJSONModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class CategoryPhoto(ORJSONModel):
    id: uuid.UUID
    bucket_name: str
    image_name: str
    category_id: uuid.UUID

    class Config:
        orm_mode = True


class Category(ORJSONModel):
    id: uuid.UUID
    name: str
    photo: Optional[CategoryPhoto]

    class Config:
        orm_mode = True


class Sale(ORJSONModel):
    id: uuid.UUID
    size: int
    good_id: uuid.UUID
    active: bool

    class Config:
        orm_mode = True


class GoodPhoto(ORJSONModel):
    id: uuid.UUID
    bucket_name: str
    image_name: str
    good_id: uuid.UUID

    class Config:
        orm_mode = True


class Size(ORJSONModel):
    id: uuid.UUID
    remainder: int
    size: int
    good_id: uuid.UUID

    class Config:
        orm_mode = True


class Good(ORJSONModel):
    id: uuid.UUID
    name: str
    description: str
    category: Category
    cost: decimal.Decimal
    sales: Optional[List[Sale]] = []
    photos: Optional[List[GoodPhoto]] = []
    color: Optional[Color]
    sizes: Optional[List[Size]]
    brand: Brand

    class Config:
        orm_mode = True


class GoodsSearch(ORJSONModel):
    name: Optional[str] = ""
    category_ids: Optional[List[uuid.UUID]] = []
    color_ids: Optional[List[uuid.UUID]] = []
    brand_ids: Optional[List[uuid.UUID]] = []
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class AddToCartRequest(ORJSONModel):
    good_id: uuid.UUID
    size_id: uuid.UUID
    count: Optional[int] = 1


class DeleteFromCartRequest(ORJSONModel):
    good_id: uuid.UUID
    size_id: uuid.UUID


class CreateSize(ORJSONModel):
    good_id: uuid.UUID
    size: int
    remainder: int


class SetSizeRemainder(ORJSONModel):
    size_id: uuid.UUID
    remainder: int


class Cart(ORJSONModel):
    good_id: uuid.UUID
    size_id: uuid.UUID

    count: int

    class Config:
        orm_mode = True
