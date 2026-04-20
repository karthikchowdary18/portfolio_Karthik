from fastapi import APIRouter, HTTPException, Response, status

from app.database.db import (
    count_projects,
    create_project,
    delete_project,
    list_projects,
    update_project,
)
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "project_count": count_projects()}


@router.get("/projects", response_model=list[Project])
async def list_projects_route(featured_only: bool = False):
    return list_projects(featured_only=featured_only)


@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project_route(payload: ProjectCreate):
    return create_project(payload)


@router.put("/projects/{project_id}", response_model=Project)
async def update_project_route(project_id: int, payload: ProjectUpdate):
    project = update_project(project_id, payload)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_route(project_id: int):
    deleted = delete_project(project_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
