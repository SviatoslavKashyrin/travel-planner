from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, services
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Planner API",
    description="API for managing travel projects and places using the Art Institute of Chicago API."
)


# ==========================================
# PROJECTS ENDPOINTS
# ==========================================

@app.post("/projects", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    if project.places and len(project.places) > 10:
        raise HTTPException(status_code=400, detail="A project can have a maximum of 10 places.")

    new_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)


    if project.places:
        seen_external_ids = set()
        for place_data in project.places:
            if place_data.external_id in seen_external_ids:
                continue
            seen_external_ids.add(place_data.external_id)


            exists = await services.verify_place_exists(place_data.external_id)
            if not exists:
                continue

            new_place = models.Place(project_id=new_project.id, **place_data.model_dump())
            db.add(new_place)

        db.commit()
        db.refresh(new_project)

    return new_project


@app.get("/projects", response_model=List[schemas.ProjectOut])
def list_projects(
        skip: int = Query(0, description="Pagination skip"),
        limit: int = Query(10, description="Pagination limit"),
        db: Session = Depends(get_db)
):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects


@app.get("/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, project_update: schemas.ProjectBase, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = project_update.name
    project.description = project_update.description
    project.start_date = project_update.start_date
    db.commit()
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.is_visited for place in project.places):
        raise HTTPException(status_code=400, detail="Cannot delete project containing visited places.")

    db.delete(project)
    db.commit()
    return None


# ==========================================
# PLACES ENDPOINTS
# ==========================================

@app.post("/projects/{project_id}/places", response_model=schemas.PlaceOut, status_code=status.HTTP_201_CREATED)
async def add_place_to_project(project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")


    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="A project can have a maximum of 10 places.")


    if any(p.external_id == place.external_id for p in project.places):
        raise HTTPException(status_code=400, detail="Place already exists in this project.")


    exists = await services.verify_place_exists(place.external_id)
    if not exists:
        raise HTTPException(status_code=400, detail="Invalid place ID. Not found in Art Institute API.")

    new_place = models.Place(project_id=project_id, **place.model_dump())
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place


@app.get("/projects/{project_id}/places", response_model=List[schemas.PlaceOut])
def list_places(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.places


@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceOut)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.project_id == project_id, models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@app.put("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceOut)
def update_place(project_id: int, place_id: int, place_update: schemas.PlaceCreate, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.project_id == project_id, models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    place.notes = place_update.notes
    place.is_visited = place_update.is_visited
    db.commit()
    db.refresh(place)
    return place