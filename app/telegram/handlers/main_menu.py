import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from app.configreader import config
from app.db import queries

from .. import keyboards as kb
from ..filters import NewUserFilter


logger = logging.getLogger(__name__)

router = Router()


@router.message(NewUserFilter())
async def new_user_handler(message: Message, state: FSMContext, session: AsyncSession):
    logger.debug(f'New user: {message.from_user.id}')

    await queries.insert_user(session, message.from_user.id)
    await main_menu_handler(message, state)


@router.message(Command(commands="start"), StateFilter(state="*"))
@router.message(F.text == '🏠 Главное меню', StateFilter(state="*"))
async def main_menu_handler(message: Message, state: FSMContext):
    await message.answer(
        'Привет',
        reply_markup=kb.to_main_menu()
    )
    await message.answer_document(config.files.presentation)
    await state.clear()
