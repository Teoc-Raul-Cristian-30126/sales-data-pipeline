CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    CONSTRAINT uq_dim_product_product_id UNIQUE (product_id)
);

CREATE TABLE warehouse.dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    CONSTRAINT uq_dim_store_store_id UNIQUE (store_id)
);

CREATE TABLE warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL
);

CREATE TABLE warehouse.fact_sales (
    sale_key BIGSERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,

    CONSTRAINT uq_fact_sales_sale_id UNIQUE (sale_id),

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key)
        REFERENCES warehouse.dim_product(product_key),

    CONSTRAINT fk_fact_sales_store
        FOREIGN KEY (store_key)
        REFERENCES warehouse.dim_store(store_key)
);



INSERT INTO warehouse.dim_product (
    product_id,
    product_name,
    category
)
SELECT
    product_id,
    product_name,
    category
FROM products
ON CONFLICT (product_id) DO NOTHING;



INSERT INTO warehouse.dim_store (
    store_id,
    store_name,
    city
)
SELECT
    store_id,
    store_name,
    city
FROM stores
ON CONFLICT (store_id) DO NOTHING;



INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    year,
    month,
    month_name,
    quarter,
    day_of_month,
    day_of_week,
    day_name
)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER AS date_key,
    d::DATE AS full_date,
    EXTRACT(YEAR FROM d)::INTEGER AS year,
    EXTRACT(MONTH FROM d)::INTEGER AS month,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(QUARTER FROM d)::INTEGER AS quarter,
    EXTRACT(DAY FROM d)::INTEGER AS day_of_month,
    EXTRACT(ISODOW FROM d)::INTEGER AS day_of_week,
    TO_CHAR(d, 'Day') AS day_name
FROM generate_series(
    (SELECT MIN(sale_date) FROM sales),
    (SELECT MAX(sale_date) FROM sales),
    INTERVAL '1 day'
) AS dates(d)
ON CONFLICT (date_key) DO NOTHING;



SELECT COUNT(*) AS products FROM warehouse.dim_product;
SELECT COUNT(*) AS stores FROM warehouse.dim_store;
SELECT COUNT(*) AS dates FROM warehouse.dim_date;



INSERT INTO warehouse.fact_sales (
    sale_id,
    date_key,
    product_key,
    store_key,
    quantity,
    unit_price,
    total_amount
)
SELECT
    s.sale_id,
    TO_CHAR(s.sale_date, 'YYYYMMDD')::INTEGER AS date_key,
    p.product_key,
    st.store_key,
    s.quantity,
    s.unit_price,
    ROUND((s.quantity * s.unit_price)::NUMERIC, 2) AS total_amount
FROM sales s
JOIN warehouse.dim_product p
    ON s.product_id = p.product_id
JOIN warehouse.dim_store st
    ON s.store_id = st.store_id
ON CONFLICT (sale_id) DO NOTHING;



SELECT COUNT(*) AS total_sales
FROM warehouse.fact_sales;



SELECT
    sale_id,
    quantity,
    unit_price,
    total_amount
FROM warehouse.fact_sales
ORDER BY sale_id
LIMIT 10;