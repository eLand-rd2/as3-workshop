from pydantic import BaseModel
from typing import Optional


# Category 基本模型
class CategoryBase(BaseModel):
    name: str


# 用于创建新類別的模型
class CategoryCreate(CategoryBase):
    pass


# 用于更新類別的模型
class CategoryUpdate(BaseModel):
    name: Optional[str] = None


# 用于读取類別信息的模型
class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True
