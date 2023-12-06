from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import standart_panel, back_panel, backback_panel, edit_panel, change_panel
from functions.function import check_float, check_name, check_size
from database.connection import (check_product_id, check_transaction_id, show_product, delete_product, 
                                 delete_transactions, check_amount_for_edit_item, update_item, 
                                 update_transaction, check_amount_for_edit_sale, show_transaction)
from handlers.prime_handlers import FSMFillForm


# initialize router
router: Router = Router()
# create dict of items
change_item_dict: dict = {}
change_sale_dict: dict = {}


flag_mode_edit: int = 0

# this handler send text if user chose command additem
@router.message(F.text == '/edititem', StateFilter(default_state))
async def send_edititem(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)


# this handler send text if user chose command change item
@router.message(F.text == LEXICON_RU['change_item'], StateFilter(FSMFillForm.fill_mode_edit))
async def send_mode_edit(message: Message, state: FSMContext):
    global flag_mode_edit
    flag_mode_edit = 1
    await message.answer(text=LEXICON_RU['chose_product_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_item)



# this handler send text if user chose command change item
@router.message(F.text == LEXICON_RU['change_sale'], StateFilter(FSMFillForm.fill_mode_edit))
async def send_mode_edit(message: Message, state: FSMContext):
    global flag_mode_edit
    flag_mode_edit = 2
    await message.answer(text=LEXICON_RU['chose_sale_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_sale)


# this handler send text if user chose command change item
@router.message(F.text == LEXICON_RU['delete_item'], StateFilter(FSMFillForm.fill_mode_edit))
async def send_mode_edit(message: Message, state: FSMContext):
    global flag_mode_edit
    flag_mode_edit = 3
    await message.answer(text=LEXICON_RU['chose_product_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_item)


# this handler send text if user chose command change item
@router.message(F.text == LEXICON_RU['delete_sale'], StateFilter(FSMFillForm.fill_mode_edit))
async def send_mode_edit(message: Message, state: FSMContext):
    global flag_mode_edit
    flag_mode_edit = 4
    await message.answer(text=LEXICON_RU['chose_sale_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_sale)


# this handler on if user input mode edit wrong
@router.message(StateFilter(FSMFillForm.fill_mode_edit))
async def send_mode_edit_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    

# this handler send text if user chose command on item
@router.message(StateFilter(FSMFillForm.fill_id_item),
                lambda x: check_product_id(x.from_user.id,  x.text))
async def send_mode_edit(message: Message, state: FSMContext):
    product_id: int = int(message.text) 
    global flag_mode_edit
    if flag_mode_edit == 1:
        user_id: int = int(message.from_user.id)
        change_item_dict[user_id] = {}
        change_item_dict[user_id]['product_id'] = product_id
        text: str = show_product(product_id, user_id)
        await message.answer(text=text, parse_mode='HTML')
        await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                            reply_markup=change_panel)
        await state.set_state(FSMFillForm.fill_name_edit)
    if flag_mode_edit == 3:
        text: str = delete_product(product_id)
        await message.answer(text=text, parse_mode='HTML', 
                            reply_markup=standart_panel)
        await state.clear()
        del change_item_dict[user_id]


# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_id_item), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_id_item_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit) 


# this handler on if user input mode edit wrong
@router.message(StateFilter(FSMFillForm.fill_id_item))
async def send_id_item_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=back_panel)


# this handler send text if user chose command on sale
@router.message(StateFilter(FSMFillForm.fill_id_sale),
                lambda x: check_transaction_id(x.from_user.id,  x.text))
async def send_mode_edit(message: Message, state: FSMContext):
    transaction_id: int = int(message.text)
    global flag_mode_edit
    if flag_mode_edit == 2:
        user_id: int = message.from_user.id
        change_sale_dict[user_id] = {}
        change_sale_dict[user_id]['transaction_id'] = transaction_id
        text: str = show_transaction(transaction_id, user_id)
        await message.answer(text=text, parse_mode='HTML')
        await message.answer(text=LEXICON_RU['right_price_sale'], parse_mode='HTML', 
                            reply_markup=change_panel)
        await state.set_state(FSMFillForm.fill_price_sale_edit)
    if flag_mode_edit == 4:
        await message.answer(text=LEXICON_RU['deleted'], parse_mode='HTML',
                             reply_markup=standart_panel)
        delete_transactions(transaction_id)
        await state.clear()
        

# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_id_sale), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_id_sale_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['change_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit) 


# this handler on if user input mode edit wrong
@router.message(StateFilter(FSMFillForm.fill_id_sale))
async def send_mode_edit_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=back_panel)
    

# this handler on if user input item name correctly 
@router.message(StateFilter(FSMFillForm.fill_name_edit), 
                lambda x: check_name(x.text))
async def send_name_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_size'], parse_mode='HTML', 
                         reply_markup=change_panel)
    user_id:int = message.from_user.id
    change_item_dict[user_id]['name'] = message.text
    await state.set_state(FSMFillForm.fill_size_edit)


# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_name_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_name_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['chose_product_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_item) 


# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_name_edit), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_name_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_name_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_size'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_size_edit) 


# this handler on if user input item name wrong
@router.message(StateFilter(FSMFillForm.fill_name_edit))
async def send_name_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=change_panel)
    

# this handler on if user input item size correctly
@router.message(StateFilter(FSMFillForm.fill_size_edit),
                lambda x: check_size(x.text))
async def send_size_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=change_panel)
    user_id: int = message.from_user.id
    change_item_dict[user_id]['size'] = message.text.upper()
    await state.set_state(FSMFillForm.fill_price_edit)


# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_size_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_size_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_item'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_name_edit)


# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_size_edit), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_name_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_size_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_price_edit) 


# this handler on if user input item size wrong
@router.message(StateFilter(FSMFillForm.fill_size_edit))
async def send_size_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=change_panel)
    
    
# this handler on if user input item price 
@router.message(StateFilter(FSMFillForm.fill_price_edit),
                lambda x: check_float(x.text))
async def send_buy_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount'], parse_mode='HTML', 
                         reply_markup=change_panel)
    user_id: int = message.from_user.id
    change_item_dict[user_id]['price'] = float(message.text)
    await state.set_state(FSMFillForm.fill_amount_edit)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_size'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_size_edit) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_price_edit), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_size_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)    


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_price_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_amount_edit)    
    
    
 # this handler on if user input item price wrong
@router.message(StateFilter(FSMFillForm.fill_price_edit))
async def send_buy_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=change_panel)   


# this handler on if user input item amount
@router.message(StateFilter(FSMFillForm.fill_amount_edit),
                lambda x: check_amount_for_edit_item(change_item_dict[x.from_user.id]['product_id'], x.text))
async def send_amount_right(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    change_item_dict[user_id]['amount'] = int(message.text)
    text: str = LEXICON_RU['right_update']
    update_item(change_item_dict[user_id])
    del change_item_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_amount_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_amount_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_price_edit) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_amount), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_amount_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)      


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_amount_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    if len(change_item_dict[user_id]) == 1:
        text: str = LEXICON_RU['unchanged']
    else:
        text: str = LEXICON_RU['right_update']
        update_item(change_item_dict[user_id])
    del change_item_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    

# this handler on if user input item amount wrong
@router.message(StateFilter(FSMFillForm.fill_amount_edit))
async def send_amount_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    

# this handler on if user input sale price 
@router.message(StateFilter(FSMFillForm.fill_price_sale_edit),
                lambda x: check_float(x.text))
async def send_buy_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount_sale'], parse_mode='HTML', 
                         reply_markup=change_panel)
    user_id: int = message.from_user.id
    change_sale_dict[user_id]['price'] = float(message.text)
    await state.set_state(FSMFillForm.fill_amount_sale_edit)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price_sale_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['chose_sale_id'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_id_sale) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_price_sale_edit), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_size_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)    


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_price_sale_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount_sale'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_amount_sale_edit)    
    
    
 # this handler on if user input sale price wrong
@router.message(StateFilter(FSMFillForm.fill_price_sale_edit))
async def send_buy_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=change_panel)   


# this handler on if user input sale amount
@router.message(StateFilter(FSMFillForm.fill_amount_sale_edit),
                lambda x: check_amount_for_edit_sale(change_sale_dict[x.from_user.id]['transaction_id'], x.text))
async def send_amount_right(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    change_sale_dict[user_id]['amount'] = int(message.text)
    text: str = LEXICON_RU['right_update']
    update_transaction(change_sale_dict[user_id])
    del change_sale_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_amount_sale_edit), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_amount_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price_sale'], parse_mode='HTML', 
                         reply_markup=change_panel)
    await state.set_state(FSMFillForm.fill_price_sale_edit) 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_amount_sale_edit), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_amount_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/edit_item'], parse_mode='HTML', 
                         reply_markup=edit_panel)
    await state.set_state(FSMFillForm.fill_mode_edit)      


# this handler om if user choose dont change
@router.message(StateFilter(FSMFillForm.fill_amount_sale_edit), 
                lambda x: x.text == LEXICON_RU['dont_change'])
async def send_name_back(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    if len(change_sale_dict[user_id]) == 1:
        text: str = LEXICON_RU['unchanged']
    else:
        text: str = LEXICON_RU['right_update']
        update_transaction(change_sale_dict[user_id])
    del change_sale_dict[user_id]
    await message.answer(text=text, parse_mode='HTML', 
                         reply_markup=standart_panel)
    await state.clear()
    

# this handler on if user input sale amount wrong
@router.message(StateFilter(FSMFillForm.fill_amount_sale_edit))
async def send_amount_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)