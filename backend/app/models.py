from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    workouts: List['Workout'] = Relationship(back_populates='owner')

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key='user.id')
    date: str
    activity: str
    duration_minutes: int
    notes: Optional[str] = None
    owner: Optional[User] = Relationship(back_populates='workouts')
