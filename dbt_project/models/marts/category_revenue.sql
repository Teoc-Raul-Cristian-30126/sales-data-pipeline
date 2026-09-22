SELECT
    p.category,
    SUM(s.total_amount) AS total_revenue,
    COUNT(DISTINCT s.sale_id) AS number_of_sales,
    SUM(s.quantity) AS total_quantity
FROM {{ ref('stg_sales') }} s
JOIN warehouse.dim_product p
    ON s.product_key = p.product_key
GROUP BY
    p.category
ORDER BY
    total_revenue DESC