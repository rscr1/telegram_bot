from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU


router: Router = Router()

# this handler on if user send other message
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(text=LEXICON_RU['other'], parse_mode='HTML')