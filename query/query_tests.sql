SELECT *
FROM warehouse.monthly_revenue
ORDER BY year, month;

SELECT *
FROM warehouse.category_revenue
ORDER BY total_revenue DESC;

SELECT *
FROM warehouse.store_revenue
ORDER BY total_revenue DESC;

SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM stores;
SELECT COUNT(*) FROM sales;