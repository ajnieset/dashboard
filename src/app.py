from pathlib import Path
from typing import Final

from litestar import Litestar, get
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar.utils.module_loader import module_to_os_path

from .db import provide_transaction, sqlalchemy_config

DEFAULT_MODULE_NAME = "src"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


@get("")
async def health() -> dict:
    return {"status": "Healthy"}


app = Litestar(
    [health],
    dependencies={"conn": provide_transaction},
    plugins=[SQLAlchemyPlugin(sqlalchemy_config)],
)
