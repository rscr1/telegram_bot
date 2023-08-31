from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import standart_panel, cancel_panel, back_panel, backback_panel
from functions.function import check_name, check_float, check_size, check_int
from database.connection import add_data
from handlers.prime_handlers import FSMFillForm

# initialize router
router: Router = Router()
# create dict of items
data_dict : dict= {}

# this handler send text if user chose command additem
@router.message(F.text == '/additem', StateFilter(default_state))
async def send_additem(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    user_id = message.from_user.id
    data_dict[user_id] = {}
    await state.set_state(FSMFillForm.fill_name)
    
    
# this handler on if user input item name correctly 
@router.message(StateFilter(FSMFillForm.fill_name), 
                lambda x: check_name(x.text))
async def send_name_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_size'], parse_mode='HTML', 
                         reply_markup=back_panel)
    user_id:int = message.from_user.id
    data_dict[user_id]['name'] = message.text
    await state.set_state(FSMFillForm.fill_size)


# this handler on if user input item name wrong
@router.message(StateFilter(FSMFillForm.fill_name))
async def send_name_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    

# this handler on if user input item size correctly
@router.message(StateFilter(FSMFillForm.fill_size),
                lambda x: check_size(x.text))
async def send_size_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    user_id: int = message.from_user.id
    data_dict[user_id]['size'] = message.text.upper()
    await state.set_state(FSMFillForm.fill_price)


# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_size), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_size_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.fill_name)


# this handler on if user input item size wrong
@router.message(StateFilter(FSMFillForm.fill_size))
async def send_size_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    
    
# this handler on if user input item price 
@router.message(StateFilter(FSMFillForm.fill_price),
                lambda x: check_float(x.text))
async def send_buy_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    user_id: int = message.from_user.id
    data_dict[user_id]['price'] = float(message.text)
    await state.set_state(FSMFillForm.fill_amount)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_size'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_size) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_price), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_size_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.fill_name)       
    
    
 # this handler on if user input item price wrong
@router.message(StateFilter(FSMFillForm.fill_price))
async def send_buy_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)   


# this handler on if user input item amount
@router.message(StateFilter(FSMFillForm.fill_amount),
                lambda x: check_int(x.text))
async def send_amount_right(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    data_dict[user_id]['amount'] = int(message.text)
    product_id = add_data(user_id, data_dict[user_id])
    text = LEXICON_RU['product_id'] + f'<code>{product_id}</code>' + '\n' + LEXICON_RU['right_status']
    del data_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_amount), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_amount_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_price) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_amount), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_amount_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                         reply_markup=cancel_panel)
    await state.set_state(FSMFillForm.fill_name)      


# this handler on if user input item amount wrong
@router.message(StateFilter(FSMFillForm.fill_amount))
async def send_amount_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)