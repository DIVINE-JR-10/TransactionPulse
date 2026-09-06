-- ============================================
-- TransactionPulse - Phase 8 SQL Analytics
-- Database: PostgreSQL
-- ============================================


-- Query 1: Top 10 Merchants by Revenue
SELECT
    m.merchant_id,
    m.merchant_name,
    m.merchant_category,
    SUM(t.amount) AS total_revenue
FROM transactions t
JOIN merchants m
    ON t.merchant_id = m.merchant_id
WHERE t.status = 'SUCCESS'
GROUP BY
    m.merchant_id,
    m.merchant_name,
    m.merchant_category
ORDER BY total_revenue DESC
LIMIT 10;


-- Query 2: Monthly Transaction Trend
SELECT
    DATE_TRUNC('month', timestamp) AS month,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY DATE_TRUNC('month', timestamp)
ORDER BY month;


-- Query 3: Top 10 Customers by Spending
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    SUM(t.amount) AS total_spent
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_spent DESC
LIMIT 10;


-- Query 4: Payment Method Analysis
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    ROUND(AVG(amount), 2) AS average_transaction
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- Query 5: Transaction Status Analysis
SELECT
    status,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM transactions
GROUP BY status
ORDER BY total_transactions DESC;


-- Query 6: Top 10 Customers by Number of Transactions
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_spent
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_transactions DESC
LIMIT 10;


-- Query 7: Merchant Category Analysis
SELECT
    m.merchant_category,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction
FROM transactions t
JOIN merchants m
    ON t.merchant_id = m.merchant_id
WHERE t.status = 'SUCCESS'
GROUP BY m.merchant_category
ORDER BY total_revenue DESC;


-- Query 8: Daily Transaction Trend
SELECT
    DATE(timestamp) AS transaction_date,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY DATE(timestamp)
ORDER BY transaction_date;


-- Query 9: Customer Type Analysis
SELECT
    c.customer_type,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY c.customer_type
ORDER BY total_revenue DESC;


-- Query 10: City-wise Transaction Analysis
SELECT
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY c.city
ORDER BY total_revenue DESC;
