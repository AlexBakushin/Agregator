import json

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
from fill import main

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Старт бота
    :param message:
    :return:
    """
    await message.answer(f"Hi, {message.from_user.full_name}!")


@router.message(F.text)
async def register_two(message: Message):
    """
    Работа с ботом
    :param message:
    :return:
    """
    try:
        answer = await main(json.loads(message.text))
        await message.answer(answer)
    except Exception as e:
        await message.answer(
            'Невалидный запос. Пример запроса:\n'
            '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')
