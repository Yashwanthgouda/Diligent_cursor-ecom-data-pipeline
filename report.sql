SELECT
    c.customer_id,
    c.name AS customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(oi.quantity), 0) AS total_items,
    COALESCE(SUM(oi.quantity * oi.item_price), 0) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.order_id
LEFT JOIN products p ON p.product_id = oi.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;


