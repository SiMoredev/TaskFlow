from fastapi import APIRouter, Depends

from app.crud.project import create_project, get_projects_for_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead
from app.api.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.post("/", response_model=ProjectRead)
async def create_project_api(
    data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_project(
        session,
        name=data.name,
        owner=current_user,
    )

@router.get("/", response_model=list[ProjectRead])
async def read_projects(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_projects_for_user(session, owner=current_user)