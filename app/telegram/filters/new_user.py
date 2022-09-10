from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import queries


class NewUserFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return await queries.get_user_id(session, message.from_user.id) is None
