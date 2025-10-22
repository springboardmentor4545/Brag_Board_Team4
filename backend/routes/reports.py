from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

@router.post("/", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    if not report.item_id and not report.comment_id:
        raise HTTPException(status_code=400, detail="Either item_id or comment_id must be provided")

    if report.item_id:
        db_item = db.query(models.Item).filter(models.Item.id == report.item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

    if report.comment_id:
        db_comment = db.query(models.Comment).filter(models.Comment.id == report.comment_id).first()
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")

    db_report = models.Report(**report.dict(), reporter_id=current_user.id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/", response_model=List[schemas.Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    reports = db.query(models.Report).offset(skip).limit(limit).all()
    return reports
