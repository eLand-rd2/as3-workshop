import dataclasses


@dataclasses.dataclass
class BrandRead:
    id: int
    name: str
    # 如果我想要把momo跟蝦皮上對應品牌的code value 加入資料表中一起存
    # value: str


@dataclasses.dataclass
class BrandCreate:
    name: str
    # value: str


@dataclasses.dataclass
class BrandUpdate:
    id: int
    name: str
    # value: str
