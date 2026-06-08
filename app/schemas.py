from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None
    is_visited: bool = False

class PlaceCreate(PlaceBase):
    pass

class PlaceOut(PlaceBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True



class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = []

class ProjectOut(ProjectBase):
    id: int
    is_completed: bool
    places: List[PlaceOut] = []

    class Config:
        from_attributes = True