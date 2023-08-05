from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from cntr.database import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from cntr.auth.models import User


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(String(1000), index=True)
    owner_id = Column(Integer, ForeignKey("b2b.user.id"))
    owner = relationship("User", back_populates="items")


class Msg(BaseModel):
    msg: str


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class ItemRead(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
