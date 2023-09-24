## https://t.me/poison_resale_bot
## Python TelegramBot Aiogram + Postgresql
***
The bot is created to simplify the process of buying and selling items on the Poison trading platform.
Among the features:
>- Calculation of order total
>- Checking the margin and markup on products to make purchasing decisions
>- Getting currency exchange rates
>- Storage of data on products and sales
>- Displaying data on products and sales
>- Editing data
***
## Includes:
>- Parsing
>- OOP
>- Functional programming
>- Decorators
>- FSM
***
## Folders
>- config.py - Initialization of data from the .env file
>- connection.py - Operations with the Postgresql database
>- function.py - All functions used in the bot
>- handlers - Folder containing files for working with FSM when clicking on a button on the main keyboard
>- keyboards.py - All keyboards used in the project
>- lexicon.py - All bot dialogs and auxiliary phrases for working with the database
>- value.py - File for parsing a website with information about the current currency exchange rate
>- .env - All personal data of the bot (see example below)
>- .gitignore - Instruction for ignoring secret files
>- bot.py - Bot's entry point

E.G  `.env`:
```
BOT_TOKEN=your_bot_api_token
ADMINS_IDS=your_admins_ids
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```
***
## Version(check file requirements + pip install -r .\requirements.txt)
>- Python 3.10.11
>- Aiogram 3.0.0b7
>- Environs 9.5.0
>- Requests 2.31.0
>- Jsonschema 4.17.3
>- Psycopg2 2.9.7
