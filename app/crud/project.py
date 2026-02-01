from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.user import User

async def create_project(session: AsyncSession, *,name: str, owner: User) -> Project:
    project = Project(name=name, owner_id=owner.id)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project

async def get_projects_for_user(session: AsyncSession, *, owner: User) -> list[Project]:
    stmt = select(Project).where(Project.owner_id == owner.id)
    result = await session.execute(stmt)
    return result.scalars().all()