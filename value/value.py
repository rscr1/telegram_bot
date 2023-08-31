import requests
import json

from lexicon.lexicon import LEXICON_RU

MONTHS: list = ['Января', 'Февраля', 'Марта', 'Апреля', 
                'Мая', 'Июня', 'Июля', 'Августа', 
                'Сентября', 'Октября', 'Ноября', 'Декабря']
DICT_MONHTS: dict = {num: month for num, month in zip(range(1, 13), MONTHS)}

URL: str = 'https://www.cbr-xml-daily.ru/daily_json.js'
responce = requests.get(URL)
data = json.loads(responce.text)

value_cny: float = data["Valute"]["CNY"]["Value"]
value_usd: float = data["Valute"]["USD"]["Value"]
previous_cny: float = data["Valute"]["CNY"]["Previous"]
previous_usd: float = data["Valute"]["USD"]["Previous"]
difference_cny: float = round(value_cny - previous_cny, 4)
difference_usd: float = round(value_usd - previous_usd, 4)
date: str = data['Date'].split('T')[0]
year, month, day = date.split('-')
date: str = day + ' ' + DICT_MONHTS[int(month)] + ' ' + year
time: str = ':'.join(data['Date'].split('T')[1].split('+')[0].split(':')[:-1])

mark_cny: str = LEXICON_RU['up'] if difference_cny >= 0 else LEXICON_RU['bottom']
mark_usd: str = LEXICON_RU['up'] if difference_usd >= 0 else LEXICON_RU['bottom']

date: str = LEXICON_RU['date'] + date + '\n' 
time: str = LEXICON_RU['time'] + time + '\n'
cny: str = LEXICON_RU['cny'] + str(value_cny) + ' (' + str(difference_cny) + mark_cny + ')' + '\n' 
usd: str = LEXICON_RU['usd'] + str(value_usd) + ' (' + str(difference_usd) + mark_usd + ')' 

information: str = date + time + cny + usd