from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.models import User


class UserRepository(SQLAlchemyAsyncRepository):
    model_type = User
