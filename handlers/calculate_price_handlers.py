from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON_RU
from keyboard.keyboards import cancel_panel, back_panel, backback_panel, course_panel, mode_panel, else_panel
from functions.function import check_float, calculate_price, zeros, check_int
from handlers.prime_handlers import FSMFillForm
from value.value import value_cny


router: Router = Router()

flag_mode: int = 0
sum_items: list[float] = []
item: dict[float, float, float, float, float, float] = {
    'course': 0.0,
    'price': 0.0,
    'amount': 0.0,
    'tax': 0.0,
    'course_weight': 0.0 ,
    'weight': 0.0,
    'static_weight': 0.0  
}


#this handler on if user choose command calculateprice and switch bot in state waiting
@router.message(F.text == '/calculateprice', StateFilter(default_state))
async def send_calculateprice_right(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course)
    zeros(item)
    sum_items.clear()
    
    
# this handler on if user choose our course
@router.message(StateFilter(FSMFillForm.choose_course),
                lambda x: x.text == LEXICON_RU['button_our'],)
async def send_choose_course_our(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_course_our'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_course)
    
    
# this handler on if user bank course
@router.message(StateFilter(FSMFillForm.choose_course),
                lambda x: x.text == LEXICON_RU['button_cny'] + f' {value_cny}' )
async def send_choose_course_cny(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_course_cny'], parse_mode='HTML', 
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_price_item)
    item['course'] = value_cny
    # print(item)
    
    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.choose_course))
async def send_choose_course_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=course_panel)
    
    
# this  handler om if user choose fill course is correctly
@router.message(StateFilter(FSMFillForm.fill_course),
                lambda x: check_float(x.text))
async def send_fill_course(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_course_cny'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_price_item)
    item['course'] = float(message.text.replace(',', '.'))
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_course), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_course_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course)    
    
    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_course))
async def send_course_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=cancel_panel)


# this  handler om if user choose fill price is correctly
@router.message(StateFilter(FSMFillForm.fill_price_item),
                lambda x: check_float(x.text))
async def send_fill_price(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_amount_item)
    item['price'] = float(message.text.replace(',', '.'))
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price_item), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_back(message: Message, state: FSMContext):
    if item['course'] == value_cny:
        await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                            reply_markup=course_panel)
        await state.set_state(FSMFillForm.choose_course) 
    else:
        await message.answer(text=LEXICON_RU['right_course_our'], parse_mode='HTML', 
                            reply_markup=back_panel)
        await state.set_state(FSMFillForm.fill_course) 
    
 
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_price_item), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_price_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)
    
    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_price_item))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=back_panel)  


# this  handler om if user choose fill amount is correctly
@router.message(StateFilter(FSMFillForm.fill_amount_item),
                lambda x: check_int(x.text))
async def send_fill_amount(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_choose_mode'], parse_mode='HTML', 
                         reply_markup=mode_panel)
    await state.set_state(FSMFillForm.choose_mode)
    item['amount'] = int(message.text)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_amount_item), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_amount_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_course_cny'], parse_mode='HTML',
                         reply_markup=back_panel)
    await state.set_state(FSMFillForm.fill_price_item)
    
 
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_amount_item), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_amount_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)
    
    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_amount_item))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)     
    
    
# this handler on if user choose mode_1
@router.message(StateFilter(FSMFillForm.choose_mode),
                lambda x: x.text == LEXICON_RU['button_mode_1'])
async def send_mode_1(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_tax'], parse_mode='HTML',
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_tax)
    global flag_mode
    flag_mode = 1
    item['static_weight'] = 0.0
    
    
# this handler on if user choose mode_2
@router.message(StateFilter(FSMFillForm.choose_mode),
                lambda x: x.text == LEXICON_RU['button_mode_2'])
async def send_mode_2(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price_kg'], parse_mode='HTML',
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_price_weight)
    global flag_mode
    flag_mode = 2
    item['tax'] = 0.0
    item['static_weight'] = 0.0
       
    
# this handler on if user choose mode_3
@router.message(StateFilter(FSMFillForm.choose_mode),
                lambda x: x.text == LEXICON_RU['button_mode_3'])
async def send_mode_3(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_tax'], parse_mode='HTML',
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_tax)
    global flag_mode
    flag_mode = 3
    item['course_weight'] = 0.0
    item['weight'] = 0.0
    
    
# this handler on if user choose mode_4
@router.message(StateFilter(FSMFillForm.choose_mode),
                lambda x: x.text == LEXICON_RU['button_mode_4'])
async def send_mode_4(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_fix'], parse_mode='HTML',
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_static_weight)
    global flag_mode
    flag_mode = 4
    item['tax'] = 0.0
    item['course_weight'] = 0.0
    item['weight'] = 0.0
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.choose_mode), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_mode_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_amount'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_amount_item)
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.choose_mode), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_mode_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)

    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.choose_mode))
async def send_course_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=mode_panel)
    
    
# this handler on if user choose tax
@router.message(StateFilter(FSMFillForm.fill_tax),
                lambda x: check_float(x.text))
async def send_tax(message: Message, state: FSMContext):
    if flag_mode == 1:
        await state.set_state(FSMFillForm.fill_price_weight)
        await message.answer(text=LEXICON_RU['right_price_kg'], parse_mode='HTML',
                         reply_markup=backback_panel)
    elif flag_mode == 3:
        await state.set_state(FSMFillForm.fill_static_weight)
        await message.answer(text=LEXICON_RU['right_fix'], parse_mode='HTML',
                         reply_markup=backback_panel)
    item['tax'] = float(message.text.replace(',', '.'))
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_tax), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_tax_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_choose_mode'], parse_mode='HTML', 
                         reply_markup=mode_panel)
    await state.set_state(FSMFillForm.choose_mode)  
    item['tax'] = 0.0
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_tax), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_size_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)
    
    
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_tax))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    
    
# this handler on if user choose price_weight
@router.message(StateFilter(FSMFillForm.fill_price_weight),
                lambda x: check_float(x.text))
async def send_price_weight(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_kg'], parse_mode='HTML',
                        reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_weight)
    item['course_weight'] = float(message.text.replace(',', '.'))
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_price_weight), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_price_weight_back(message: Message, state: FSMContext):
    if flag_mode == 1:
        await message.answer(text=LEXICON_RU['right_tax'], parse_mode='HTML',
                         reply_markup=backback_panel)
        await state.set_state(FSMFillForm.fill_tax)
    elif flag_mode == 2:
        await message.answer(text=LEXICON_RU['right_choose_mode'], parse_mode='HTML', 
                         reply_markup=mode_panel)
        await state.set_state(FSMFillForm.choose_mode) 
    item['course_weight'] = 0.0 
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_price_weight), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_price_weight_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)

   
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_price_weight))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)

  
 # this handler on if user fill_weight_1
@router.message(StateFilter(FSMFillForm.fill_weight),
                lambda x: check_float(x.text))
async def send_weight_1(message: Message, state: FSMContext):
    item['weight'] = float(message.text.replace(',', '.')) 
    sum_items.append(calculate_price(**item))
    await message.answer(text=LEXICON_RU['right_calculate_price'] +
                         str(calculate_price(**item)) + 
                         LEXICON_RU['rubles']+ '\n' +
                         LEXICON_RU['total_price'] + 
                         str(round(sum(sum_items), 2)) + 
                         LEXICON_RU['rubles'], 
                         parse_mode='HTML',
                        reply_markup=else_panel)
    await state.set_state(FSMFillForm.fill_choose_else)
    # print(item)
    
  
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_weight), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_weight_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['right_price_kg'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    await state.set_state(FSMFillForm.fill_price_weight) 
    item['weight'] = 0.0  
  
  
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_weight), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_weight_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course)  
    zeros(item)
  

# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_weight))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=course_panel)
  

# this handler on if user choose static_weight_3
@router.message(StateFilter(FSMFillForm.fill_static_weight),
                lambda x: check_float(x.text))
async def send_static_weight_4(message: Message, state: FSMContext):
    item['static_weight'] = float(message.text.replace(',', '.'))
    sum_items.append(calculate_price(**item))
    await message.answer(text=LEXICON_RU['right_calculate_price'] +
                         str(calculate_price(**item)) + 
                         LEXICON_RU['rubles'] + '\n' +
                         LEXICON_RU['total_price'] + 
                         str(round(sum(sum_items), 2)) + 
                         LEXICON_RU['rubles'], parse_mode='HTML',
                        reply_markup=else_panel)
    await state.set_state(FSMFillForm.fill_choose_else)
    # print(item)      
      
      
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_static_weight), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_static_weight_back(message: Message, state: FSMContext):
    if flag_mode == 3:
        await message.answer(text=LEXICON_RU['right_tax'], parse_mode='HTML',
                         reply_markup=backback_panel)
        await state.set_state(FSMFillForm.fill_tax)
    elif flag_mode == 4:
        await message.answer(text=LEXICON_RU['right_choose_mode'], parse_mode='HTML', 
                         reply_markup=mode_panel)
        await state.set_state(FSMFillForm.choose_mode) 
    item['static_weight'] = 0.0
      
      
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_static_weight), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_static_weight_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)
    
      
# this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_static_weight))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=backback_panel)
    
    
# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_choose_else), 
                lambda x: x.text == LEXICON_RU['button_else'])
async def send_size_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    zeros(item)
    
    
# this handler om if user choose back
@router.message(StateFilter(FSMFillForm.fill_choose_else), 
                lambda x: x.text == LEXICON_RU['button_back'])
async def send_choose_else_back(message: Message, state: FSMContext):
    if flag_mode in [1, 2]:
        await message.answer(text=LEXICON_RU['right_kg'], parse_mode='HTML',
                        reply_markup=backback_panel)
        await state.set_state(FSMFillForm.fill_weight)
    elif flag_mode in [3, 4]:
        await message.answer(text=LEXICON_RU['right_fix'], parse_mode='HTML',
                         reply_markup=backback_panel)
        await state.set_state(FSMFillForm.fill_static_weight)
    sum_items.pop()
    

# this handler om if user choose backback    
@router.message(StateFilter(FSMFillForm.fill_choose_else), 
                lambda x: x.text == LEXICON_RU['button_backback'])
async def send_else_backback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/calculate_price'], parse_mode='HTML', 
                         reply_markup=course_panel)
    await state.set_state(FSMFillForm.choose_course) 
    sum_items.pop()
    zeros(item)    
    
    
 # this handler on if user input wrong
@router.message(StateFilter(FSMFillForm.fill_choose_else))
async def send_fill_wrong(message: Message):
    await message.answer(text=LEXICON_RU['error_input'], parse_mode='HTML', 
                         reply_markup=else_panel)   