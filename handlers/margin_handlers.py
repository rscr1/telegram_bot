from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import standart_panel, cancel_panel, back_panel
from functions.function import check_float, calculate_margin
from handlers.prime_handlers import FSMFillForm


router: Router = Router()

buy_price: float = 0.
sale_price: float = 0.

# this handler on if user chose command /calculatemargin
@router.message(F.text == '/calculatemargin', StateFilter(default_state))
async def process_alculatemargin_command(message: Message, state: FSMContext):
    await message.answer(text = LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.calculate_margin_buy)
    
    
# this handler send calculate item margin buy, if input is correctly
@router.message(StateFilter(FSMFillForm.calculate_margin_buy), 
                lambda x: check_float(x.text))
async def send_margin_buy_right(message: Message, state: FSMContext):
    global buy_price
    buy_price = float(message.text)
    await message.answer(text=LEXICON_RU['right_sale'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.calculate_margin_sale)
    
    
# this handler send calculate item margin buy, if input isn't correctly
@router.message(StateFilter(FSMFillForm.calculate_margin_buy))
async def send_margin_buy_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    
    
# this handler send calculate item margin sale, if input is correctly
@router.message(StateFilter(FSMFillForm.calculate_margin_sale), 
                lambda x: check_float(x.text))
async def send_margin_sale_right(message: Message, state: FSMContext):
    global buy_price, sale_price
    sale_price = float(message.text)
    await message.answer(text=calculate_margin(buy_price, sale_price), parse_mode='HTML', 
                         reply_markup=standart_panel)
    buy_price, sale_price = 0., 0.
    await state.clear()
    
    
# this handler on if user choose back
@router.message(StateFilter(FSMFillForm.calculate_margin_sale), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_margin_sale_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.calculate_margin_buy)
    global buy_price
    buy_price = 0.
    
    
    
# this handler send calculate item margin sale, if input isn't correctly
@router.message(StateFilter(FSMFillForm.calculate_margin_sale))
async def send_margin_sale_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=back_panel)