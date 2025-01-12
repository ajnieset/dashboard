from dataclasses import asdict, dataclass

from litestar import Router, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.repositories import UserRepository


@dataclass
class UserCreate:
    email: str
    name: str


@get("/")
async def get_users(db_session: AsyncSession) -> list[User]:
    repo = UserRepository(session=db_session)
    return await repo.list()


@get("/{user_id:int}")
async def get_user(user_id: int, db_session: AsyncSession) -> User:
    repo = UserRepository(session=db_session)
    return await repo.get(user_id)


@post("/")
async def create_user(data: UserCreate, db_session: AsyncSession) -> User:
    repo = UserRepository(session=db_session)
    return await repo.add(User(**asdict(data)))


@delete("/{user_id:int}")
async def delete_user(user_id: int, db_session: AsyncSession) -> None:
    repo = UserRepository(session=db_session)
    await repo.delete(user_id)


user_router = Router("/users", route_handlers=[get_users, create_user, get_user, delete_user])
