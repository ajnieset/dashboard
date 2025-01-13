import datetime
from dataclasses import dataclass
from hashlib import sha256

from litestar import Router, post, status_codes
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.repositories import UserRepository


@dataclass
class LoginResponse:
    access_token: str
    token_type: str


@dataclass
class UserLogin:
    username: str
    password: str


@post("/")
async def login(data: UserLogin, db_session: AsyncSession) -> LoginResponse:
    repo = UserRepository(session=db_session)
    user: User = await repo.get(User.email == data.username)
    if user.password_hash != sha256(data.password.encode()).hexdigest():
        raise HTTPException(status_code=status_codes.HTTP_401_UNAUTHORIZED)
    token = datetime.datetime.now().isoformat()
    return {"access_token": sha256(token.encode()).hexdigest(), "token_type": "bearer"}


login_router = Router("/login", route_handlers=[login])
