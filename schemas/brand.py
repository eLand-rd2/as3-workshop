import dataclasses


@dataclasses.dataclass
class BrandRead:
    id: int
    name: str


@dataclasses.dataclass
class BrandCreate:
    name: str


@dataclasses.dataclass
class BrandUpdate:
    id: int
    name: str
