from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Item Schemas
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)

# Comment Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    item_id: int
    owner_id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)

# Reaction Schemas
class ReactionBase(BaseModel):
    reaction_type: str

class ReactionCreate(ReactionBase):
    pass

class Reaction(ReactionBase):
    id: int
    item_id: int
    owner_id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)

# Report Schemas
class ReportBase(BaseModel):
    reason: str
    item_id: Optional[int] = None
    comment_id: Optional[int] = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    reporter_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
