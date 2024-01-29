from pydantic import BaseModel
from typing import Optional, List


# 基本模型
class BrandBase(BaseModel):
    name: str
    ecommerce: Optional[str] = None


# 創建模型
class BrandCreate(BrandBase):
    pass


# 更新模型
class BrandUpdate(BaseModel):
    name: Optional[str] = None
    ecommerce: Optional[str] = None


# 閱讀模型
class BrandRead(BrandBase):
    id: int

    class Config:
        orm_mode = True
