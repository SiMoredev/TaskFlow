from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router

from app.db.session import get_session

app = FastAPI()
app.include_router(auth_router)
app.include_router(projects_router)

@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": result.scalar()}
