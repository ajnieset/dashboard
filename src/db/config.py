from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Final

from advanced_alchemy.extensions.litestar import AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.plugins.sqlalchemy import AlembicAsyncConfig
from litestar.utils.module_loader import module_to_os_path


DEFAULT_MODULE_NAME = "src"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///dashboard.sqlite",
    before_send_handler="autocommit",
    session_config=session_config,
    create_all=True, # you probably dont want this for anything but testing
    alembic_config=AlembicAsyncConfig(
        script_config=f"{BASE_DIR}/db/migrations/alembic.ini",
        script_location=f"{BASE_DIR}/db/migrations",
    ),
)
