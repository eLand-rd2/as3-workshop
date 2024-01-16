import dataclasses

from schemas.brand import BrandRead


@dataclasses.dataclass
class ProductRead:
    id: int
    name: str
    brand: 'BrandRead'


@dataclasses.dataclass
class ProductCreate:
    name: str
    brand_id: int


@dataclasses.dataclass
class ProductUpdate:
    id: int
    name: str
    brand_id: int
