from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import standart_panel, cancel_panel, back_panel, backback_panel
from functions.function import check_float
from database.connection import check_id_not_sold, show_row, check_amount, add_sale
from handlers.prime_handlers import FSMFillForm

# initialize router
router: Router = Router()
# create dict of items
sale_dict : dict= {}

# this handler send text if user chose command addsale
@router.message(F.text == '/addsale', StateFilter(default_state))
async def send_addsale(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_sale'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    user_id: int = message.from_user.id
    sale_dict[user_id] = {}
    await state.set_state(FSMFillForm.fill_id)


# this handler send text if user input id item correctly 
@router.message(StateFilter(FSMFillForm.fill_id),
                lambda x: check_id_not_sold(x.from_user.id,  x.text))
async def send_id_sale(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    product_id: int = int(message.text)
    sale_dict[user_id]['product_id'] = product_id
    text: str = show_row(user_id, message.text)
    await message.answer(text=text, parse_mode='HTML')
    await message.answer(text=LEXICON_RU['right_price_sale'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_price_sale)


# this handler send text if user input id item wrong
@router.message(StateFilter(FSMFillForm.fill_id))
async def send_id_sale_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=cancel_panel)


# this handler on if user input sale price 
@router.message(StateFilter(FSMFillForm.fill_price_sale),
                lambda x: check_float(x.text))
async def send_price_sale(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount_sale'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    user_id: int = message.from_user.id
    sale_dict[user_id]['price'] = float(message.text)
    await state.set_state(FSMFillForm.fill_amount_sale)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price_sale), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_sale_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_sale'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.fill_id)


 # this handler on if user input sale price wrong
@router.message(StateFilter(FSMFillForm.fill_price_sale))
async def send_price_sale_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=back_panel)
    

# this handler on if user input sale amount
@router.message(StateFilter(FSMFillForm.fill_amount_sale),
                lambda x: check_amount(sale_dict[x.from_user.id]['product_id'], x.text))
async def send_amount_sale(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    amount: int = int(message.text)
    sale_dict[user_id]['amount'] = amount
    transactions_id: int = add_sale(sale_dict[user_id])
    text: str = LEXICON_RU['sale_id'] + f'<code>{transactions_id}</code>' + '\n' + LEXICON_RU['right_status_sale']
    del sale_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    
    
# this handler on if user choose back
@router.message(StateFilter(FSMFillForm.fill_amount_sale), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_amount_sale_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price_sale'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_price_sale) 
    
    
# this handler on if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_amount_sale), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_amount_sale_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_sale'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.fill_id)     


# this handler on if user input sale wrong
@router.message(StateFilter(FSMFillForm.fill_amount_sale))
async def send_show_mode_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)