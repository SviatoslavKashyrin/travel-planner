from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)

    places = relationship("Place", back_populates="project", cascade="all, delete-orphan")

    @property
    def is_completed(self):
        if not self.places:
            return False
        return all(place.is_visited for place in self.places)


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    external_id = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    is_visited = Column(Boolean, default=False)

    project = relationship("Project", back_populates="places")