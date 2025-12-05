SELECT 
    m.item_name, 
    SUM(d.quantity) as total_sold
FROM OrderDetails d
JOIN MenuItems m ON d.item_id = m.item_id
GROUP BY m.item_name
ORDER BY total_sold DESC
LIMIT 3;

SELECT 
    u.full_name as waiter_name, 
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue
FROM Orders o
JOIN Users u ON o.user_id = u.user_id
GROUP BY u.full_name
ORDER BY total_revenue DESC;

SELECT 
    DATE(order_date) as report_date, 
    COUNT(order_id) as order_count,
    SUM(total_amount) as daily_total
FROM Orders
GROUP BY DATE(order_date)
ORDER BY report_date DESC;

SELECT 
    c.category_name, 
    SUM(d.subtotal) as category_revenue
FROM OrderDetails d
JOIN MenuItems m ON d.item_id = m.item_id
JOIN Categories c ON m.category_id = c.category_id
GROUP BY c.category_name;

SELECT AVG(total_amount) as average_check_value FROM Orders;

CREATE OR REPLACE FUNCTION get_total_sales(start_date DATE, end_date DATE)
RETURNS DECIMAL AS $$
DECLARE
    total_sales DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(total_amount), 0) INTO total_sales
    FROM Orders
    WHERE DATE(order_date) BETWEEN start_date AND end_date;
    
    RETURN total_sales;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE DeletedOrdersLog (
    log_id SERIAL PRIMARY KEY,
    order_id INT,
    deleted_at TIMESTAMP DEFAULT NOW(),
    user_who_deleted VARCHAR(50) -- Supabase'de genelde auth.uid() kullanılır ama basit tutalım
);

CREATE OR REPLACE FUNCTION log_deleted_order()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO DeletedOrdersLog (order_id, user_who_deleted)
    VALUES (OLD.order_id, 'System_Admin');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_delete_order
AFTER DELETE ON Orders
FOR EACH ROW
EXECUTE FUNCTION log_deleted_order();