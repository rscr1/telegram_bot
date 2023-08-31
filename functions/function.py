import re


from lexicon.lexicon import LEXICON_RU


# this fucntion calculate price of item
def calculate_price(**kwargs) -> float:
    cost: list = list(kwargs.values())
    price_without_send: float = cost[0] * cost[1]
    amount: int = cost[2]
    tax: float = cost[3]
    price_send: float = cost[4] * cost[5] + cost[6]
    return round(amount * (price_without_send + tax + price_send), 2)


# this function check what input it's size
def check_size(size: str) -> bool:
    if not isinstance(size, str):
        return False
    if size.upper() == 'ONE SIZE':
        return True
    if len(size) > 8:
        return False
    sizes_1: list = ['S', 'M', 'L']
    sizes_2: list = ['XS', 'XL']
    sizes_3: list = ['XXS', 'XXL']
    sizes_4: list = ['XXXS', 'XXXL']
    sizes_list: list[list] = [sizes_1, sizes_2, sizes_3, sizes_4]
    size: str = size.upper().strip()
    
    if size.__contains__(',') and not size.__contains__('.'):
        if size[-1] != ',':
            part: bool = size.split(',')
            if 0 < len(part[0]) < 3 and len(part[1]) == 1:
                if part[0].isdigit() and part[1].isdigit():
                    return True
    
    elif size.__contains__('.') and not size.__contains__(','):
        if size[-1] != '.':
            part: bool = size.split('.')
            if 0 < len(part[0]) < 3 and len(part[1]) == 1:
                if part[0].isdigit() and part[1].isdigit():
                    return True
       
    elif not size.__contains__('.') and not size.__contains__(','):
        if size.isdigit() and 5 < int(size) < 56:
            return True
        elif size.isalpha():
            for length, sizes in zip(list(range(1, 5)), sizes_list):
                if len(size) == length and size in sizes:
                    return True     
    return False


# this function calculate marig
def calculate_margin(buy: str, sale: str) -> str:
    buy: float = float(buy)
    sale: float = float(sale)
    margin_number: float = round(float(sale) - float(buy), 1)
    marginality_number:float = round(margin_number / sale * 100, 1)
    extra_number: float = round(margin_number / buy * 100, 1)
    margin: str = LEXICON_RU['margin'] + str(margin_number) + LEXICON_RU['rubles'] + '\n'
    marginality: str = LEXICON_RU['marginality'] + str(marginality_number) + ' %\n'
    extra: str = LEXICON_RU['extra'] + str(extra_number) + ' %\n'
    mark: str = {marginality_number < 15: LEXICON_RU['shit'], 14 < marginality_number < 25: LEXICON_RU['good'], marginality_number > 24: LEXICON_RU['nice']}[True]
    return  margin + marginality + extra + mark


# this function check that input it's price
def check_float(price: str) -> bool:
    if not isinstance(price, str):
        return False
    try:
        value = float(price)
        if 0 < value <= 10**6:
            decimals = str(value).split('.')[-1]
            if len(decimals) < 2:
                return True
    except ValueError:
        pass
    return False 


# this function make dict to start view
def zeros(dict: dict[float]) -> dict[float]:
    for key in dict:
        dict[key] = 0.0
    return dict


# this function check that input it's name item
def check_name(name: str) -> bool:
    if name in (LEXICON_RU['dont_change'], LEXICON_RU['button_back'], LEXICON_RU['button_backback']) :
        return False
    if not isinstance(name, str):
        return False
    if len(name) > 40:
        return False
    return True


# this fucntion check that input it's amount item
def check_int(amount: str) -> bool:
    if not isinstance(amount, str):
        return False
    if amount.isdigit():
        amount = int(amount)
        if 2**31 > amount > 0:
            return True
    return False