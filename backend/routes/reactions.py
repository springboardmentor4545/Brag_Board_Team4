from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/items/{item_id}/reactions",
    tags=["reactions"],
)

@router.post("/", response_model=schemas.Reaction)
def create_reaction_for_item(item_id: int, reaction: schemas.ReactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if the user has already reacted to this item
    db_reaction = db.query(models.Reaction).filter(models.Reaction.item_id == item_id, models.Reaction.owner_id == current_user.id).first()
    if db_reaction:
        # If reaction exists, update it
        db_reaction.reaction_type = reaction.reaction_type
        db.commit()
        db.refresh(db_reaction)
        return db_reaction

    db_reaction = models.Reaction(**reaction.dict(), owner_id=current_user.id, item_id=item_id)
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

@router.get("/", response_model=List[schemas.Reaction])
def read_reactions_for_item(item_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reactions = db.query(models.Reaction).filter(models.Reaction.item_id == item_id).offset(skip).limit(limit).all()
    return reactions

@router.delete("/{reaction_id}", status_code=204)
def delete_reaction(reaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_reaction = db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Reaction not found")
    if db_reaction.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reaction")
    db.delete(db_reaction)
    db.commit()
    return
