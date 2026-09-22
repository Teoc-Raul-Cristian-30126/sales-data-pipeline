SELECT
    st.store_id,
    st.store_name,
    st.city,
    SUM(s.total_amount) AS total_revenue,
    COUNT(DISTINCT s.sale_id) AS number_of_sales,
    SUM(s.quantity) AS total_quantity
FROM {{ ref('stg_sales') }} s
JOIN warehouse.dim_store st
    ON s.store_key = st.store_key
GROUP BY
    st.store_id,
    st.store_name,
    st.city
ORDER BY
    total_revenue DESC