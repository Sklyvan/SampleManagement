import enum
from uuid import uuid4

from sqlalchemy import Column, String, Date, Enum

from app.db.base import Base

class SampleType(enum.Enum):
    blood = "blood"
    saliva = "saliva"
    tissue = "tissue"

class StatusType(enum.Enum):
    collected = "collected"
    processing = "processing"
    archived = "archived"

class Sample(Base):
    __tablename__ = "samples"

    sample_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    sample_type = Column(Enum(SampleType), nullable=False)
    subject_id = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    status = Column(Enum(StatusType), nullable=False)
    storage_location = Column(String, nullable=False)
