SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM stores;
SELECT COUNT(*) FROM sales;

-- Checking the data relationships

SELECT
    s.sale_id,
    s.sale_date,
    p.product_name,
    p.category,
    st.store_name,
    st.city,
    s.quantity,
    s.unit_price,
    s.quantity * s.unit_price AS total_amount
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
JOIN stores st
    ON s.store_id = st.store_id
LIMIT 10;

-- Which product category generates the highest revenue

SELECT
    p.category,
    SUM(s.quantity * s.unit_price) AS total_revenue
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Monthly revenue

SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY month
ORDER BY month;