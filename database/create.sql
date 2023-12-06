CREATE TABLE IF NOT EXISTS product
(
    product_id SERIAL PRIMARY KEY,
    user_id bigint NOT NULL,
    product_name varchar(40) NOT NULL,
    product_size varchar(8) NOT NULL,
    product_price numeric(8, 2) NOT NULL,
    product_amount integer NOT NULL,
    product_date date NOT NULL,
    product_total numeric(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions
(
    transaction_id SERIAL PRIMARY KEY,
    product_id bigint NOT NULL,
    price numeric(8, 2) NOT NULL,
    amount integer NOT NULL,
    date date NOT NULL,
    total numeric(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);
