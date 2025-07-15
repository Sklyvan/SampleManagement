from datetime import date

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
