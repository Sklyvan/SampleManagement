from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.db.models import SampleType, StatusType

class SampleCreate(BaseModel):
    sample_type: SampleType
    subject_id: str
    collection_date: date
    status: StatusType
    storage_location: str

class SampleRead(SampleCreate):
    sample_id: str

    class Config:
        from_attributes = True

class SampleUpdate(BaseModel):
    sample_type: Optional[SampleType]
    subject_id: Optional[str]
    collection_date: Optional[date]
    status: Optional[StatusType]
    storage_location: Optional[str]
