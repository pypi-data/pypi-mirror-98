from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, event


# SQLAlchemy models...
class TimeStampMixin(object):
    """ Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


# Pydantic models...
class CntrBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True


class PluginOptionModel(CntrBase):
    pass
