from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, verify_password

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()

async def create_user(session: AsyncSession, *, email: str, password: str) -> User:
    user = User(email=email, hashed_password=hash_password(password), is_active=True)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user