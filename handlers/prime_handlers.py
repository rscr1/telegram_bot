from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import standart_panel
from value.value import information


router: Router = Router()

class FSMFillForm(StatesGroup):
    
    choose_course = State()
    fill_course = State()
    fill_price_item = State()
    fill_amount_item = State()
    choose_mode =  State()
    fill_tax = State()
    fill_price_weight = State()
    fill_weight = State()
    fill_static_weight = State()
    fill_print = State()
    fill_choose_else = State()
    
    calculate_margin_buy = State()
    calculate_margin_sale = State()
    
    fill_name = State()
    fill_size = State()
    fill_price = State()
    fill_amount = State()

    choose_time = State()
    all_time = State()
    last_month = State()
    show_item = State()

    fill_id = State()
    fill_price_sale = State()
    fill_amount_sale = State()

    fill_mode_edit = State()
    fill_id_item = State()
    fill_id_sale = State()
    fill_name_edit = State()
    fill_size_edit = State()
    fill_price_edit = State()
    fill_amount_edit = State()

    fill_price_sale_edit = State()
    fill_amount_sale_edit = State()


# this handler on if user start bot, contain information of Bot
@router.message(F.text == '/start', StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text = LEXICON_RU['/start'], parse_mode='HTML', 
                         reply_markup=standart_panel)
        
  
# this handler on if user chose command help, contain Bot commands list
@router.message(F.text == '/help', StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], parse_mode='HTML', 
                         reply=standart_panel)
    
    
# this handler on if user chose command cancel, cancel other command
@router.message(F.text == '/cancel', ~StateFilter(default_state))
async def cancel_command_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'], parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    
    
# this handler in if user chose command cancel, but other command off
@router.message(F.text == '/cancel', StateFilter(default_state))
async def cancel_command_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_cancel'], parse_mode='HTML')
    
    
# this handler on if user chose command /getcourse
@router.message(F.text == '/getcourse', StateFilter(default_state))
async def process_getcourse_command(message: Message):
    await message.answer(text = information, parse_mode='HTML', 
                         reply_markup=standart_panel)