from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserModel


async def insert_user(
    session: AsyncSession,
    telegram_id: int,
) -> None:
    session.add(
        UserModel(
            telegram_id=telegram_id
        )
    )
    await session.commit()


async def get_user_id(
    session: AsyncSession,
    telegram_id: int = None,
    discord_id: int = None,
    phone_number: str = None
) -> int:
    
    if not any([telegram_id, discord_id, phone_number]):
        raise ValueError('At least one argument must be provided')

    stmt = select(UserModel.id)

    if telegram_id:
        stmt = stmt.where(UserModel.telegram_id == telegram_id)

    if discord_id:
        stmt = stmt.where(UserModel.discord_id == discord_id)

    if phone_number:
        stmt = stmt.where(UserModel.phone_number == phone_number)

    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user(
    session: AsyncSession,
    user_id: int = None,
    telegram_id: int = None,
    discord_id: int = None,
    phone_number: str = None
) -> UserModel:

    if not any([user_id, telegram_id, discord_id, phone_number]):
        raise ValueError('At least one argument must be provided')

    stmt = select(UserModel)

    if user_id:
        stmt = stmt.where(UserModel.id == user_id)

    if telegram_id:
        stmt = stmt.where(UserModel.telegram_id == telegram_id)
    
    if discord_id:
        stmt = stmt.where(UserModel.discord_id == discord_id)
    
    if phone_number:
        stmt = stmt.where(UserModel.phone_number == phone_number)

    result = await session.execute(stmt)
    return result.scalars().first()

