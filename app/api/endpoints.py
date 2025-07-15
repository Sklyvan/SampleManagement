from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas.sample import SampleCreate, SampleRead, SampleUpdate
from app.db.models import Sample, SampleType, StatusType
from app.db.session import get_db

router = APIRouter()

@router.post("/samples", response_model=SampleRead)
def create_sample(sample: SampleCreate, db: Session = Depends(get_db)) -> SampleRead:
    """
    Create a new sample in the database.
    :param sample: SampleCreate schema containing the details of the sample to be created.
    :param db: Database session dependency.
    :return: SampleRead schema containing the details of the created sample.
    """
    db_sample = Sample(**sample.model_dump())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

@router.get("/samples/{sample_id}", response_model=SampleRead)
def read_sample(sample_id: str, db: Session = Depends(get_db)) -> SampleRead:
    """
    Retrieve a sample by its ID.
    :param sample_id: The ID of the sample to retrieve.
    :param db: Database session dependency.
    :return: SampleRead schema containing the details of the retrieved sample.
    """
    db_sample = db.query(Sample).filter(Sample.sample_id == sample_id).first()
    if not db_sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    else:
        return db_sample

@router.get("/samples", response_model=List[SampleRead])
def read_samples(
    sample_status: Optional[StatusType] = Query(None, description="Filter by sample status"),
    sample_type: Optional[SampleType] = Query(None, description="Filter by sample type"),
    db: Session = Depends(get_db)) -> List[SampleRead]:
    """
    Retrieve all samples from the database.
    :param sample_type: Filter by sample type (e.g., blood, saliva, tissue).
    :param sample_status: Filter by sample status (e.g., collected, processing, archived).
    :param db: Database session dependency.
    :return: List of SampleRead schemas containing the details of all samples.
    """
    query = db.query(Sample)

    if sample_status:
        query = query.filter(Sample.status == sample_status)
    if sample_type:
        query = query.filter(Sample.sample_type == sample_type)

    return query.all()

@router.delete("/samples/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(sample_id: str, db: Session = Depends(get_db)) -> None:
    """
    Delete a sample by its ID.
    :param sample_id: The ID of the sample to delete.
    :param db: Database session dependency.
    """
    db_sample = db.query(Sample).filter(Sample.sample_id == sample_id).first()
    if not db_sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    else:
        db.delete(db_sample)
        db.commit()

@router.put("/samples/{sample_id}", response_model=SampleRead)
def update_sample(sample_id: str, update_data: SampleUpdate, db: Session = Depends(get_db)) -> SampleRead:
    """
    Update an existing sample in the database based on its ID.
    :param sample_id: The ID of the sample to update.
    :param update_data: SampleUpdate schema containing the fields to update.
    :param db: Database session dependency.
    :return: SampleRead schema containing the updated sample details.
    """
    sample = db.query(Sample).filter(Sample.sample_id == sample_id).first()

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    else:
        update_dict = update_data.model_dump(exclude_unset=True)

        for field, value in update_dict.items():
            setattr(sample, field, value)

        db.commit()
        db.refresh(sample)
        return sample
