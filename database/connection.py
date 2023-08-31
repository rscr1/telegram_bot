import psycopg2
import datetime
import decimal
from config_data.config  import Config, load_config
from lexicon.lexicon import COLUMNS_SHOW_ALL, COLUMNS_SHOW_SOLD, COLUMNS_SHOW_SELLING, COLUMNS_EDIT, LEXICON_RU


# load config to variable config
config: Config = load_config()

# initialize host, database, user, password
host = config.tg_bot.host
database = config.tg_bot.database
user = config.tg_bot.user
password = config.tg_bot.password



#this function translate data to text
def to_text(name_columns: str, output_text) -> str:
    underline: str = '\n' + '=' * len(name_columns) + '\n'
    text: str =  f'<code>{name_columns + underline + output_text}</code>'
    return text


# this fucntion add item to database
def add_data(user_id: int, data_dict: dict) -> None:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    today = datetime.date.today() 
    product_name, product_size, product_price, product_amount = data_dict.values()
    product_total: float = product_price * product_amount
    insert_query: str = '''
                        INSERT INTO product (user_id, product_name, product_size, product_price, product_amount, product_date, product_total) 
                        VALUES 
                            (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING product_id;'''
    cursor.execute(insert_query, (user_id, product_name, product_size, product_price, product_amount, today, product_total))
    product_id: str = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return product_id


# this function check id
def check_id_not_sold(user_id: int, product_id: int) -> bool:
    if not isinstance(product_id, str):
        return False
    if not product_id.isdigit():
        return False
    product_id: int = int(product_id)
    if product_id == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_id,
                            product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0)
                        FROM
                            product
                            LEFT JOIN transactions USING (product_id)
                        WHERE
                            user_id = %s;'''
    cursor.execute(insert_query, (user_id,))
    input: list = cursor.fetchall()
    cursor.close()
    conn.close()
    product_ids: list = []
    [product_ids.append(i) for i, j in input if j > 0]
    return product_id in product_ids


#this function show  item from database
def show_row(user_id: int, product_id) -> str:
    columns: list = COLUMNS_SHOW_ALL
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_id, product_name, product_size, product_price, 
                            product_amount, product_date, product_total,
                            product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0)
                        FROM 
                            product 
                            LEFT JOIN transactions USING (product_id)
                        WHERE  
                            user_id = %s 
                            AND product_id = %s;'''
    cursor.execute(insert_query, (user_id, product_id))
    input: list = cursor.fetchall()[0]
    output: list = []
    for cell in input:
        if isinstance(cell, decimal.Decimal):
            output.append(str(float(cell)))
        elif isinstance(cell, datetime.date):
            output.append('.'.join(str(cell).split('-')[::-1]))
        elif not isinstance(cell, str):
            output.append(str(cell))
        else:
            output.append(cell)
    output_text: str = ''
    for i, cell in enumerate(output):
        if len(columns[i]) > len(cell):
            output[i] = output[i].center(len(columns[i]))
        elif len(columns[i]) < len(cell):
            columns[i] = columns[i].center(len(cell))   
        if i != len(output) - 1:
            output_text += output[i] + ' | '
        else:
            output_text += output[i]
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


# this function check amount
def check_amount(product_id: int, amount: int) -> bool:
    if not isinstance(amount, str):
        return False
    if not amount.isdigit():
        return False
    amount = int(amount)
    if amount == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_amount - COALESCE(SUM(amount) OVER (ORDER BY product_id), 0)
                        FROM
                            product
                            LEFT JOIN transactions USING (product_id)
                        WHERE
                            product_id = %s;'''
    cursor.execute(insert_query, (product_id,))
    input: int = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return input >= amount 


# this function check amount for edit item
def check_amount_for_edit_item(product_id: int, amount: int) -> bool:
    if not isinstance(amount, str):
        return False
    if not amount.isdigit():
        return False
    amount = int(amount)
    if amount == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            COALESCE(SUM(amount) OVER (ORDER BY product_id), 0)
                        FROM
                            product
                            LEFT JOIN transactions USING (product_id)
                        WHERE
                            product_id = %s;'''
    cursor.execute(insert_query, (product_id,))
    input: int = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return amount >= input


# this function check amount for edit sale
def check_amount_for_edit_sale(product_id: int, amount: int) -> bool:
    if not isinstance(amount, str):
        return False
    if not amount.isdigit():
        return False
    amount = int(amount)
    if amount == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_amount
                        FROM
                            product
                            JOIN transactions using (product_id)
                        WHERE
                            transaction_id = %s;'''
    cursor.execute(insert_query, (product_id,))
    input: int = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return amount <= input


# this function add sale to database
def add_sale(sale_dict: dict) -> None:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    today = datetime.date.today() 
    product_id,price, amount = sale_dict.values()
    total: float = price * amount
    insert_query: str = '''
                        INSERT INTO transactions (product_id, price, amount, date, total) 
                        VALUES 
                            (%s, %s, %s, %s, %s)
                            RETURNING transaction_id;'''
    cursor.execute(insert_query, (product_id, price, amount, today, total))
    transaction_id: str = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return transaction_id


#this function show all item from database
def show_all(user_id: int, flag_mode_time: int) -> str:
    columns: list = COLUMNS_SHOW_ALL
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    if flag_mode_time == 1:
        insert_query: str = '''
                            SELECT DISTINCT
                                product_id, product_name, product_size, product_price, 
                                product_amount, product_date, product_total,
                                product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0)
                            FROM 
                                product 
                                LEFT JOIN transactions USING (product_id)
                            WHERE 
                                user_id = %s
                            ORDER BY
                                product_id DESC;'''
    elif flag_mode_time == 2:
        insert_query: str = '''
                            SELECT DISTINCT
                                product_id, product_name, product_size, product_price, 
                                product_amount, product_date, product_total,
                                product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0)
                            FROM 
                                product 
                                LEFT JOIN transactions USING (product_id)
                            WHERE 
                                user_id = %s
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                product_id DESC;
                            '''
    elif flag_mode_time == 3:
        insert_query: str = '''
                            SELECT DISTINCT
                                product_id, product_name, product_size, product_price, 
                                product_amount, product_date, product_total,
                                product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0)
                            FROM 
                                product 
                                LEFT JOIN transactions USING (product_id)
                            WHERE 
                                user_id = %s
                                AND EXTRACT(DAY FROM product_date) = EXTRACT(DAY FROM CURRENT_DATE)
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                product_id DESC;
                            '''
    cursor.execute(insert_query, (user_id,))
    input: list = cursor.fetchall()
    if len(input) == 0:
        cursor.close()
        conn.close()
        return 'Данных нет'
    output: list = [[''] * len(input[0]) for _ in range(len(input))]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if isinstance(input[i][j], decimal.Decimal):
                output[i][j] = str(float(input[i][j]))
            elif isinstance(input[i][j], datetime.date):
                output[i][j] = '.'.join(str(input[i][j]).split('-')[::-1])
            elif not isinstance(input[i][j], str):
                output[i][j] = str(input[i][j])
            else:
                output[i][j] = input[i][j]
    output_text: str = ''
    max_lens: list = [len(max(column, key=len)) for column in zip(*output)]
    for i in range(len(input)):
        for j, max_len in zip(range(len(input[0])), max_lens):
            if len(columns[j]) > max_len:
                output[i][j] = output[i][j].center(len(columns[j]))
            elif len(columns[j]) < max_len:
                columns[j] = columns[j].center(max_len)
            elif len(output[i][j]) < max_len:
                output[i][j] = output[i][j].center(max_len)   
            if j != len(output[0]) - 1:
                output_text += output[i][j] + ' | '
            else:
                output_text += output[i][j]
        output_text += '\n'
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


#this function show sold item from database
def show_sold(user_id: int, flag_mode_item: int) -> str:
    columns: list = COLUMNS_SHOW_SOLD
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    if flag_mode_item == 1:
        insert_query: str = '''
                            SELECT DISTINCT
                                transaction_id, product_id, product_name, product_size, price, amount, date,
                                amount * (price - product_price)
                            FROM 
                                product
                                JOIN transactions USING (product_id)
                            WHERE
                                transaction_id IS NOT NULL
                                AND user_id = %s
                            ORDER BY
                                transaction_id DESC;'''
    elif flag_mode_item == 2:
        insert_query: str = '''
                            SELECT DISTINCT
                                transaction_id, product_id, product_name, product_size, price, amount, date,
                                amount * (price - product_price)
                            FROM 
                                product
                                JOIN transactions USING (product_id)
                            WHERE
                                transaction_id IS NOT NULL
                                AND user_id = %s
                                AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                transaction_id DESC;'''
    elif flag_mode_item == 3:
        insert_query: str = '''
                            SELECT DISTINCT
                                transaction_id, product_id, product_name, product_size, price, amount, date,
                                amount * (price - product_price)
                            FROM 
                                product
                                JOIN transactions USING (product_id)
                            WHERE
                                transaction_id IS NOT NULL
                                AND user_id = %s
                                AND EXTRACT(DAY FROM product_date) = EXTRACT(DAY FROM CURRENT_DATE)
                                AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                transaction_id DESC;'''
    cursor.execute(insert_query, (user_id,))
    input: list = cursor.fetchall()
    if len(input) == 0:
        cursor.close()
        conn.close()
        return 'Данных нет'
    output: list = [[''] * len(input[0]) for _ in range(len(input))]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if isinstance(input[i][j], decimal.Decimal):
                output[i][j] = str(float(input[i][j]))
            elif isinstance(input[i][j], datetime.date):
                output[i][j] = '.'.join(str(input[i][j]).split('-')[::-1])
            elif not isinstance(input[i][j], str):
                output[i][j] = str(input[i][j])
            else:
                output[i][j] = input[i][j]
    output_text: str = ''
    max_lens: list = [len(max(column, key=len)) for column in zip(*output)]
    for i in range(len(input)):
        for j, max_len in zip(range(len(input[0])), max_lens):
            if len(columns[j]) > max_len:
                output[i][j] = output[i][j].center(len(columns[j]))
            elif len(columns[j]) < max_len:
                columns[j] = columns[j].center(max_len)
            elif len(output[i][j]) < max_len:
                output[i][j] = output[i][j].center(max_len)   
            if j != len(output[0]) - 1:
                output_text += output[i][j] + ' | '
            else:
                output_text += output[i][j]
        output_text += '\n'
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


#this function show selling item from database
def show_selling(user_id: int, flag_mode_item: int) -> str:
    columns: list = COLUMNS_SHOW_SELLING
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    if flag_mode_item == 1:
        insert_query: str = '''
                            WITH sum_amount(product_id, remains) AS (
                                SELECT DISTINCT 
                                    product_id,
                                    product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0) AS remains
                                FROM 
                                    product
                                    LEFT JOIN transactions USING (product_id))

                            SELECT DISTINCT 
                                product.product_id,
                                product_name,
                                product_size,
                                product_price,
                                product_date,
                                remains,
                                DATE_PART('day', NOW()::DATE) - DATE_PART('day', product_date::DATE)
                            FROM
                                product
                                JOIN sum_amount USING (product_id)
                            WHERE
                                remains <> 0
                                AND user_id = %s
                            ORDER BY
                                product_id DESC;'''
    elif flag_mode_item == 2:
        insert_query: str = '''
                            WITH sum_amount(product_id, remains) AS (
                                SELECT DISTINCT 
                                    product_id,
                                    product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0) AS remains
                                FROM 
                                    product
                                    LEFT JOIN transactions USING (product_id))

                            SELECT DISTINCT 
                                product.product_id,
                                product_name,
                                product_size,
                                product_price,
                                product_date,
                                remains,
                                DATE_PART('day', NOW()::DATE) - DATE_PART('day', product_date::DATE)
                            FROM
                                product
                                JOIN sum_amount USING (product_id)
                            WHERE
                                remains <> 0
                                AND user_id = %s
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                product_id DESC;
                            '''
    elif flag_mode_item == 3:
        insert_query: str = '''
                            WITH sum_amount(product_id, remains) AS (
                                SELECT DISTINCT 
                                    product_id,
                                    product_amount - COALESCE(SUM(amount) OVER (PARTITION BY product_id ORDER BY user_id), 0) AS remains
                                FROM 
                                    product
                                    LEFT JOIN transactions USING (product_id))

                            SELECT DISTINCT 
                                product.product_id,
                                product_name,
                                product_size,
                                product_price,
                                product_date,
                                remains,
                                DATE_PART('day', NOW()::DATE) - DATE_PART('day', product_date::DATE)
                            FROM
                                product
                                JOIN sum_amount USING (product_id)
                            WHERE
                                remains <> 0
                                AND user_id = %s
                                AND EXTRACT(DAY FROM product_date) = EXTRACT(DAY FROM CURRENT_DATE)
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            ORDER BY
                                product_id DESC;
                            '''
    cursor.execute(insert_query, (user_id,))
    input: list = cursor.fetchall()
    if len(input) == 0:
        cursor.close()
        conn.close()
        return 'Данных нет'
    output: list = [[''] * len(input[0]) for _ in range(len(input))]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if j == len(input[0]) - 1:
                output[i][j] = str(int(input[i][j]))
            elif isinstance(input[i][j], decimal.Decimal):
                output[i][j] = str(float(input[i][j]))
            elif isinstance(input[i][j], datetime.date):
                output[i][j] = '.'.join(str(input[i][j]).split('-')[::-1])
            elif not isinstance(input[i][j], str):
                output[i][j] = str(input[i][j])
            else:
                output[i][j] = input[i][j]
    output_text: str = ''
    max_lens: list = [len(max(column, key=len)) for column in zip(*output)]
    for i in range(len(input)):
        for j, max_len in zip(range(len(input[0])), max_lens):
            if len(columns[j]) > max_len:
                output[i][j] = output[i][j].center(len(columns[j]))
            elif len(columns[j]) < max_len:
                columns[j] = columns[j].center(max_len)
            elif len(output[i][j]) < max_len:
                output[i][j] = output[i][j].center(max_len)   
            if j != len(output[0]) - 1:
                output_text += output[i][j] + ' | '
            else:
                output_text += output[i][j]
        output_text += '\n'
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


#this function show stat item from database
def show_stat(user_id: int, flag_mode_item: int) -> str:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    if flag_mode_item == 1:
        insert_query: str = '''
                            SELECT DISTINCT
                                SUM(DISTINCT product.product_amount) AS total_quantity_purchased,
                                SUM(DISTINCT transactions.amount) AS total_quantity_sold,
                                SUM(DISTINCT product.product_price * product.product_amount) AS total_spent,
                                SUM(DISTINCT transactions.price * transactions.amount) AS total_earned,
                                ROUND(AVG(DISTINCT transactions.price - product.product_price), 2) AS average_margin,
                                ROUND(AVG(DISTINCT transactions.price * transactions.amount - product.product_price * product.product_amount), 2) AS total_margin,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(transactions.price, 0)), 2) AS marginality,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(product.product_price, 0)), 2) AS markup
                            FROM
                                product
                                LEFT JOIN transactions USING (product_id)
                            WHERE
                                product.user_id = %s;'''
    elif flag_mode_item == 2:
        insert_query: str = '''
                            SELECT DISTINCT
                                SUM(DISTINCT product.product_amount) AS total_quantity_purchased,
                                SUM(DISTINCT transactions.amount) AS total_quantity_sold,
                                SUM(DISTINCT product.product_price * product.product_amount) AS total_spent,
                                SUM(DISTINCT transactions.price * transactions.amount) AS total_earned,
                                ROUND(AVG(DISTINCT transactions.price - product.product_price), 2) AS average_margin,
                                ROUND(AVG(DISTINCT transactions.price * transactions.amount - product.product_price * product.product_amount), 2) AS total_margin,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(transactions.price, 0)), 2) AS marginality,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(product.product_price, 0)), 2) AS markup
                            FROM
                                product
                                LEFT JOIN transactions USING (product_id)
                            WHERE
                                product.user_id = %s 
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE);
                            '''
    elif flag_mode_item == 3:
        insert_query: str = '''
                            SELECT DISTINCT
                                SUM(DISTINCT product.product_amount) AS total_quantity_purchased,
                                SUM(DISTINCT transactions.amount) AS total_quantity_sold,
                                SUM(DISTINCT product.product_price * product.product_amount) AS total_spent,
                                SUM(DISTINCT transactions.price * transactions.amount) AS total_earned,
                                ROUND(AVG(DISTINCT transactions.price - product.product_price), 2) AS average_margin,
                                ROUND(AVG(DISTINCT transactions.price * transactions.amount - product.product_price * product.product_amount), 2) AS total_margin,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(transactions.price, 0)), 2) AS marginality,
                                ROUND(100 * AVG(DISTINCT (transactions.price - product.product_price) / NULLIF(product.product_price, 0)), 2) AS markup
                            FROM
                                product
                                LEFT JOIN transactions USING (product_id)
                            WHERE
                                product.user_id = %s
                                AND EXTRACT(DAY FROM product_date) = EXTRACT(DAY FROM CURRENT_DATE)
                                AND EXTRACT(MONTH FROM product_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                                AND EXTRACT(YEAR FROM product_date) = EXTRACT(YEAR FROM CURRENT_DATE);
                            '''
    cursor.execute(insert_query, (user_id,))
    input: list = cursor.fetchall()[0]
    output: list = []
    for cell in input:
        if isinstance(cell, decimal.Decimal):
            output.append(str(float(cell)))
        elif isinstance(cell, datetime.date):
            output.append('.'.join(str(cell).split('-')[::-1]))
        elif not isinstance(cell, str):
            output.append(str(cell))
        else:
            output.append(cell)
    output_text: str = ''
    sum_amount = LEXICON_RU['sum_amount']
    sum_amount_sold = LEXICON_RU['sum_amount_sold']
    spent = LEXICON_RU['spent']
    got = LEXICON_RU['spent']
    margin = LEXICON_RU['got_margin']
    total_margin = LEXICON_RU['total_margin']
    marginality = LEXICON_RU['got_marginality']
    markup = LEXICON_RU['got_markup']
    columns = [sum_amount, sum_amount_sold, spent, got, margin, total_margin, marginality, markup]
    for i, j in zip(columns, output):
        output_text += i + j + '\n'
    return output_text


# this function show data before del or edit 
def show_product(product_id: int, user_id: int) -> str:
    columns: list = COLUMNS_EDIT
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_name, product_size, 
                            product_price, product_amount,
                            product_date,
                            COALESCE(price::text, '-'), 
                            COALESCE(amount::text, '-'), 
                            COALESCE(date::text, '-')
                        FROM
                            product pr
                            LEFT JOIN transactions USING (product_id)
                        WHERE
                            pr.product_id = %s
                            AND user_id = %s'''
    cursor.execute(insert_query, (product_id, user_id))
    input: list = cursor.fetchall()
    output: list = [[''] * len(input[0]) for _ in range(len(input))]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if isinstance(input[i][j], decimal.Decimal):
                output[i][j] = str(float(input[i][j]))
            elif isinstance(input[i][j], datetime.date):
                output[i][j] = '.'.join(str(input[i][j]).split('-')[::-1])
            elif not isinstance(input[i][j], str):
                output[i][j] = str(input[i][j])
            else:
                output[i][j] = input[i][j]
    output_text: str = ''
    max_lens: list = [len(max(column, key=len)) for column in zip(*output)]
    for i in range(len(input)):
        for j, max_len in zip(range(len(input[0])), max_lens):
            if len(columns[j]) > max_len:
                output[i][j] = output[i][j].center(len(columns[j]))
            elif len(columns[j]) < max_len:
                columns[j] = columns[j].center(max_len)
            elif len(output[i][j]) < max_len:
                output[i][j] = output[i][j].center(max_len)   
            if j != len(output[0]) - 1:
                output_text += output[i][j] + ' | '
            else:
                output_text += output[i][j]
        output_text += '\n'
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


# this function show sale
def show_transaction(transaction_id: int, user_id: int) -> str:
    columns: list = COLUMNS_EDIT
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT DISTINCT
                            product_name, product_size, 
                            product_price, product_amount,
                            product_date,
                            price,  amount, date
                        FROM
                            product 
                            LEFT JOIN transactions USING (product_id)
                        WHERE
                            transaction_id = %s
                            AND user_id = %s'''
    cursor.execute(insert_query, (transaction_id, user_id))
    input: list = cursor.fetchall()
    output: list = [[''] * len(input[0]) for _ in range(len(input))]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if isinstance(input[i][j], decimal.Decimal):
                output[i][j] = str(float(input[i][j]))
            elif isinstance(input[i][j], datetime.date):
                output[i][j] = '.'.join(str(input[i][j]).split('-')[::-1])
            elif not isinstance(input[i][j], str):
                output[i][j] = str(input[i][j])
            else:
                output[i][j] = input[i][j]
    output_text: str = ''
    max_lens: list = [len(max(column, key=len)) for column in zip(*output)]
    for i in range(len(input)):
        for j, max_len in zip(range(len(input[0])), max_lens):
            if len(columns[j]) > max_len:
                output[i][j] = output[i][j].center(len(columns[j]))
            elif len(columns[j]) < max_len:
                columns[j] = columns[j].center(max_len)
            elif len(output[i][j]) < max_len:
                output[i][j] = output[i][j].center(max_len)   
            if j != len(output[0]) - 1:
                output_text += output[i][j] + ' | '
            else:
                output_text += output[i][j]
        output_text += '\n'
    name_columns: str = ' | '.join(columns)
    cursor.close()
    conn.close()
    return to_text(name_columns, output_text)


# this function check base have product_id 
def check_product_id(user_id: int, product_id: int) -> bool:
    if not isinstance(product_id, str):
        return False
    if not product_id.isdigit():
        return False
    product_id = int(product_id)
    if product_id == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT EXISTS(
                            SELECT 1
                                FROM
                                    product
                                WHERE
                                    user_id = %s
                                    AND product_id = %s
                        );'''
    cursor.execute(insert_query, (user_id, product_id))
    input: bool = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return input


def check_transaction_id(user_id:int, transaction_id) -> bool:
    if not isinstance(transaction_id, str):
        return False
    if not transaction_id.isdigit():
        return False
    transaction_id = int(transaction_id)
    if transaction_id == 0:
        return False
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        SELECT EXISTS(
                            SELECT 1
                                FROM
                                    transactions
                                    JOIN product USING (product_id)
                                WHERE
                                    user_id = %s
                                    AND transaction_id = %s
                        );'''
    cursor.execute(insert_query, (user_id, transaction_id))
    input: bool = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return input


# this function delete product
def delete_product(product_id: int) -> str:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        DELETE FROM product
                        WHERE product_id = %s
                        RETURNING (SELECT ARRAY_AGG(transaction_id) FROM transactions WHERE product_id = %s);'''
    cursor.execute(insert_query, (product_id, product_id))
    input: tuple = cursor.fetchone()[0]
    deleted: str = LEXICON_RU['deleted'] 
    if input is None:
        conn.commit()
        cursor.close()
        conn.close()
        return deleted
    indexes: str = ', '.join(map(str, input))
    deleted += '\n' + LEXICON_RU['deleted_sale'] + f'<code>{indexes}</code>'
    conn.commit()
    cursor.close()
    conn.close()
    return deleted


# this function delete sale
def delete_transactions(transaction_id: int) -> None:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    insert_query: str = '''
                        DELETE FROM
                            transactions
                        WHERE
                            transaction_id = %s;'''
    cursor.execute(insert_query, (transaction_id, ))
    conn.commit()
    cursor.close()
    conn.close()


# this function update item
def update_item(change_data: dict) -> None:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    product_id = change_data['product_id']
    product_name = change_data.get('name', None)
    product_size = change_data.get('size', None)
    product_price = change_data.get('price', None)
    product_amount = change_data.get('amount', None)
    if product_price is not None and product_amount is not None:
        product_total = product_price * product_amount
    else:
        product_total = None
    cursor = conn.cursor()
    insert_query = '''
                    UPDATE product
                    SET 
                        product_name = COALESCE(%s, product_name),
                        product_size = COALESCE(%s, product_size),
                        product_price = COALESCE(%s, product_price),
                        product_amount = COALESCE(%s, product_amount),
                        product_total = COALESCE(%s, %s * product_amount, product_price * %s, product_total)
                    WHERE product_id = %s;'''
    cursor.execute(insert_query, (
        product_name, product_size, product_price, product_amount,
        product_total, product_price, product_amount,
        product_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


# this function update sale
def update_transaction(change_data: dict) -> None:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    transaction_id = change_data['transaction_id']
    price = change_data.get('price', None)
    amount = change_data.get('amount', None)
    if price is not None and amount is not None:
        total = price * amount
    else:
        total = None
    cursor = conn.cursor()
    insert_query = '''
                    UPDATE transactions
                    SET 
                        price = COALESCE(%s, price),
                        amount = COALESCE(%s, amount),
                        total = COALESCE(%s, %s * amount, price * %s, total)
                    WHERE transaction_id = %s;'''
    cursor.execute(insert_query, (
        price, amount,
        total, price, amount,
        transaction_id
    ))
    conn.commit()
    cursor.close()
    conn.close()