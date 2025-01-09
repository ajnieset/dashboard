from dataclasses import dataclass, asdict
from litestar import Router, get, post

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User

@dataclass
class UserCreate:
    email: str
    name: str


@get("/")
async def get_users(db_session: AsyncSession) -> list[User]:
    stmt = select(User)
    result = await db_session.execute(stmt)
    users = result.scalars().all()
    return users

@get("/{user_id:int}")
async def get_user(user_id:int, db_session: AsyncSession) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    return user

@post("/")
async def create_user(data: UserCreate, db_session: AsyncSession) -> User:
    new_user = User(**asdict(data))
    db_session.add(new_user)
    await db_session.flush()
    return new_user


user_router = Router("/users", route_handlers=[get_users, create_user, get_user])
