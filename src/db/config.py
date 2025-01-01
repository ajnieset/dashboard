from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Final

from advanced_alchemy.extensions.litestar import AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import AlembicAsyncConfig
from litestar.status_codes import HTTP_409_CONFLICT
from litestar.utils.module_loader import module_to_os_path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

DEFAULT_MODULE_NAME = "src"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite",
    before_send_handler="autocommit",
    session_config=session_config,
    create_all=True,
    alembic_config=AlembicAsyncConfig(
        script_config=f"{BASE_DIR}/db/migrations/alembic.ini",
        script_location=f"{BASE_DIR}/db/migrations",
    ),
)


async def provide_transaction(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session

    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
