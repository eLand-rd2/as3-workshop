from pydantic import BaseModel
from typing import Optional


# Sentiment 基本模型
class SentimentBase(BaseModel):
    name: str


# 用于创建新主题的模型→需要有嗎??
class SentimentCreate(SentimentBase):
    pass


# 用于更新情緒的模型
class SentimentUpdate(BaseModel):
    name: Optional[str] = None


# 用于读取主题信息的模型
class SentimentRead(SentimentBase):
    id: int

    class Config:
        from_attributes = True
