from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import show_panel, standart_panel, time_panel
from database.connection import show_all, show_sold, show_selling, show_stat
from handlers.prime_handlers import FSMFillForm

# initialize router
router: Router = Router()


flag_mode_time: int = 0

# this handler send text if user chose /showitem
@router.message(F.text == '/showitem', StateFilter(default_state))
async def send_showitem(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/show_item'], parse_mode='HTML', 
                         reply_markup=time_panel)
    await state.set_state(FSMFillForm.choose_time)


# this handler on if user choose show mode all time
@router.message(F.text == LEXICON_RU['all_time'], StateFilter(FSMFillForm.choose_time))
async def send_show_mode_all_time(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['show_time'], parse_mode='HTML', 
                         reply_markup=show_panel)
    global flag_mode_time
    flag_mode_time = 1
    await state.set_state(FSMFillForm.show_item)


# this handler on if user cho0se show mode last month
@router.message(F.text == LEXICON_RU['last_month'], StateFilter(FSMFillForm.choose_time))
async def send_show_mode_last_time(message: Message, state: FSMContext):
    global flag_mode_time
    flag_mode_time = 2
    await message.answer(text=LEXICON_RU['show_time'], parse_mode='HTML', 
                         reply_markup=show_panel)
    await state.set_state(FSMFillForm.show_item)


# this handler on if user cho0se show mode this day
@router.message(F.text == LEXICON_RU['day'], StateFilter(FSMFillForm.choose_time))
async def send_show_mode_last_time(message: Message, state: FSMContext):
    global flag_mode_time
    flag_mode_time = 3
    await message.answer(text=LEXICON_RU['show_time'], parse_mode='HTML', 
                         reply_markup=show_panel)
    await state.set_state(FSMFillForm.show_item)


# this handler on if user input item show time mode wrong
@router.message(StateFilter(FSMFillForm.choose_time))
async def send_show_mode_time_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=time_panel)


# this handler on if user chose show mode all
@router.message(F.text == LEXICON_RU['show_all'], StateFilter(FSMFillForm.show_item))
async def send_show_mode_all(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    global flag_mode_time
    text: str = show_all(user_id, flag_mode_time)
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()


# this handler on if user chose show mode sold 
@router.message(F.text == LEXICON_RU['show_sold'], StateFilter(FSMFillForm.show_item))
async def send_show_mode_sold(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    global flag_mode_time
    text: str = show_sold(user_id, flag_mode_time)
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()

    
# this handler on if user chose show mode seling
@router.message(F.text == LEXICON_RU['show_seling'], StateFilter(FSMFillForm.show_item))
async def send_show_mode_seling(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    global flag_mode_time
    text: str = show_selling(user_id, flag_mode_time)
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()


# this handler on if user chose show mode stat
@router.message(F.text == LEXICON_RU['show_stat'], StateFilter(FSMFillForm.show_item))
async def send_show_mode_stat(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    global flag_mode_time
    text: str = show_stat(user_id, flag_mode_time)
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()


# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.show_item), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_show_mode_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/show_item'], parse_mode='HTML', 
                         reply_markup=time_panel)
    await state.set_state(FSMFillForm.choose_time) 


# this handler on if user input item show mode wrong
@router.message(StateFilter(FSMFillForm.show_item))
async def send_show_mode_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=show_panel)