from pydantic import BaseModel
from typing import Optional


# Topic 基本模型
class TopicBase(BaseModel):
    name: str


# 用于创建新主题的模型
class TopicCreate(TopicBase):
    pass


# 用于更新主题的模型
class TopicUpdate(BaseModel):
    name: Optional[str] = None


# 用于读取主题信息的模型
class TopicRead(TopicBase):
    id: int

    class Config:
        orm_mode = True
