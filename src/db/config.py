from collections.abc import AsyncGenerator

from advanced_alchemy.base import BigIntAuditBase
from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import AlembicAsyncConfig
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///dashboard.sqlite",
    metadata=BigIntAuditBase.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
    alembic_config=AlembicAsyncConfig(
        script_config="./src/db/migrations/alembic.ini",
        script_location="./src/db/migrations",
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
