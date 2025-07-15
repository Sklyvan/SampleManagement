from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.sample import SampleCreate, SampleRead
from app.db.models import Sample
from app.db.session import get_db

router = APIRouter()

@router.post("/samples", response_model=SampleRead)
def create_sample(sample: SampleCreate, db: Session = Depends(get_db)) -> Sample:
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
def read_sample(sample_id: str, db: Session = Depends(get_db)) -> Sample:
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

@router.get("/samples", response_model=list[SampleRead])
def read_samples(db: Session = Depends(get_db)) -> list[Sample]:
    """
    Retrieve all samples from the database.
    :param db: Database session dependency.
    :return: List of SampleRead schemas containing the details of all samples.
    """
    db_samples = db.query(Sample).all()
    return db_samples


@router.delete("/samples/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(sample_id: str, db: Session = Depends(get_db)):
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