from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU
from value.value import value_cny


# create button name 
help: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_1'])
get_course: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_2'])
calculate_price: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_3'])
calculate_margin: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_4'])
add_item: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_5'])
show_item: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_6']) 
edit_item: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_7'])
add_sale: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_8'])

cancel: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_cancel'])

back: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_back'])
backback: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_backback'])
button_cny: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_cny'] + f' {value_cny}')
button_our: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_our'])
button_with_with: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_mode_1'])
button_without_with: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_mode_2'])
button_with_without: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_mode_3'])
button_without_without: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_mode_4'])
button_show_all: KeyboardButton = KeyboardButton(text=LEXICON_RU['show_all'])
button_show_sold: KeyboardButton = KeyboardButton(text=LEXICON_RU['show_sold'])
button_show_seling: KeyboardButton = KeyboardButton(text=LEXICON_RU['show_seling'])
button_show_stat: KeyboardButton = KeyboardButton(text=LEXICON_RU['show_stat'])
button_else: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_else'])

button_change_item: KeyboardButton = KeyboardButton(text=LEXICON_RU['change_item'])
button_change_sale: KeyboardButton = KeyboardButton(text=LEXICON_RU['change_sale'])
button_delete_item: KeyboardButton = KeyboardButton(text=LEXICON_RU['delete_item'])
button_delete_sale: KeyboardButton = KeyboardButton(text=LEXICON_RU['delete_sale'])

all_time: KeyboardButton = KeyboardButton(text=LEXICON_RU['all_time'])
last_month: KeyboardButton = KeyboardButton(text=LEXICON_RU['last_month'])
day: KeyboardButton = KeyboardButton(text=LEXICON_RU['day'])
dont_change: KeyboardButton = KeyboardButton(text=LEXICON_RU['dont_change'])

# next: KeyboardButton = KeyboardButton(text=LEXICON_RU['button_next'])

buttons: list = [help, get_course, calculate_price, calculate_margin, add_item, show_item, edit_item, add_sale]

#create button standart panel 
panel_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
panel_builder.row(*buttons, width=4)
standart_panel = panel_builder.as_markup(
                                one_time_keyboard=False,
                                resize_keyboard=True)

#create button cancel panel
cancel_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[cancel]],
                                    resize_keyboard=True)

iteration_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[cancel]],
                                    resize_keyboard=True)

back_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[back, cancel]],
                                    resize_keyboard=True)

backback_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[backback, back, cancel]],
                                    resize_keyboard=True)

course_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_our, button_cny],
                                              [cancel]],
                                    resize_keyboard=True)
mode_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_with_with, button_without_with, 
                                               button_with_without, button_without_without],
                                              [backback, back, cancel]],
                                    resize_keyboard=True)

show_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_show_all, button_show_sold, button_show_seling, button_show_stat],
                                              [back, cancel]],
                                    resize_keyboard=True)

edit_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_change_item, button_change_sale, button_delete_item, button_delete_sale],
                                              [cancel]],
                                    resize_keyboard=True)
time_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[all_time, last_month, day],
                                              [cancel]],
                                    resize_keyboard=True)

else_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_else],
                                              [backback, back, cancel]],
                                    resize_keyboard=True)


change_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[dont_change],
                                              [backback, back, cancel]],
                                    resize_keyboard=True)