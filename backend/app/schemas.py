from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterForm(BaseModel):
    email: EmailStr
    password: str

class WorkoutForm(BaseModel):
    date: str
    activity: str
    duration_minutes: int
    notes: Optional[str] = None
