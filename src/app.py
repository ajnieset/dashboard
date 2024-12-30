from litestar import Litestar, get
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from .db import db_config, provide_transaction


@get("")
async def health() -> dict:
    return {"status": "Healthy"}


app = Litestar(
    [health],
    dependencies={"conn": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
