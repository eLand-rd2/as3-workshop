import dataclasses


@dataclasses.dataclass
class BrandRead:
    id: int
    name: str
    ecommerce: str
    # 如果我想要把momo跟蝦皮上對應品牌的code value 加入資料表中一起存
    # value: str


@dataclasses.dataclass
class BrandCreate:
    name: str
    ecommerce: str = None
    # value: str


@dataclasses.dataclass
class BrandUpdate:
    id: int
    name: str = None
    ecommerce: str = None
    # value: str
