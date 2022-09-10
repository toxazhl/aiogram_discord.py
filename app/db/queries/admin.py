from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserModel, AdminModel


async def is_admin(session: AsyncSession, telegram_id: int) -> bool:
    stmt = select(AdminModel).where(AdminModel.user_id == UserModel.id).where(UserModel.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalars().first() is not None