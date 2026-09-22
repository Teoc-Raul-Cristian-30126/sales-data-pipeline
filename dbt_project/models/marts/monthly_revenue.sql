SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(s.total_amount) AS total_revenue,
    COUNT(DISTINCT s.sale_id) AS number_of_sales,
    SUM(s.quantity) AS total_quantity
FROM {{ ref('stg_sales') }} s
JOIN warehouse.dim_date d
    ON s.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month