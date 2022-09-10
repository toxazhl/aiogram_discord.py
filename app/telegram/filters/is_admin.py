from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import queries


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return await queries.is_admin(session, message.from_user.id)
