from sqlalchemy import text


TOTAL_REVENUE_QUERY = text("""
    SELECT
        COALESCE(ROUND(SUM(total_amount), 2), 0) AS total_revenue
    FROM orders
    WHERE status != 'cancelled';
""")


ITEM_REVENUE_QUERY = text("""
    SELECT
        COALESCE(
            ROUND(
                SUM(oi.quantity * oi.unit_price),
                2
            ),
            0
        ) AS item_revenue
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled';
""")


ORDER_STATUS_QUERY = text("""
    SELECT
        status,
        COUNT(*) AS order_count,
        COALESCE(ROUND(SUM(total_amount), 2), 0) AS revenue
    FROM orders
    GROUP BY status
    ORDER BY revenue DESC;
""")


GROSS_PROFIT_QUERY = text("""
    SELECT
        COALESCE(
            ROUND(
                SUM(
                    oi.quantity *
                    (oi.unit_price - oi.unit_cost)
                ),
                2
            ),
            0
        ) AS estimated_gross_profit
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled';
""")


TOP_PRODUCTS_QUERY = text("""
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        COALESCE(
            ROUND(
                SUM(oi.quantity * oi.unit_price),
                2
            ),
            0
        ) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
    ORDER BY revenue DESC
    LIMIT 10;
""")


ORDER_KPI_QUERY = text("""
    SELECT
        COUNT(*) AS total_orders,

        COUNT(*) FILTER (
            WHERE status != 'cancelled'
        ) AS active_orders,

        COUNT(*) FILTER (
            WHERE status = 'cancelled'
        ) AS cancelled_orders,

        COALESCE(
            ROUND(
                SUM(total_amount) FILTER (
                    WHERE status != 'cancelled'
                ),
                2
            ),
            0
        ) AS total_revenue

    FROM orders;
""")

PRODUCT_PERFORMANCE_QUERY = text("""
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        ROUND(
            SUM(oi.quantity * oi.unit_price),
            2
        ) AS revenue,
        ROUND(
            SUM(oi.quantity * oi.unit_cost),
            2
        ) AS cost,
        ROUND(
            SUM(
                oi.quantity *
                (oi.unit_price - oi.unit_cost)
            ),
            2
        ) AS gross_profit,
        ROUND(
            CASE
                WHEN SUM(oi.quantity * oi.unit_price) > 0
                THEN
                    (
                        SUM(
                            oi.quantity *
                            (oi.unit_price - oi.unit_cost)
                        )
                        /
                        SUM(oi.quantity * oi.unit_price)
                    ) * 100
                ELSE 0
            END,
            2
        ) AS gross_margin
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
    ORDER BY revenue DESC;
""")

CUSTOMER_ANALYTICS_QUERY = text("""
    WITH latest_date AS (
        SELECT MAX(signup_date) AS max_signup_date
        FROM customers
    )
    SELECT
        COUNT(*) AS total_customers,
        COUNT(*) FILTER (
            WHERE signup_date >= max_signup_date - INTERVAL '89 days'
              AND signup_date <= max_signup_date
        ) AS new_customers
    FROM customers
    CROSS JOIN latest_date;
""")
CUSTOMER_ORDER_VALUE_QUERY = text("""
    SELECT
        COALESCE(
            ROUND(
                SUM(oi.quantity * oi.unit_price) /
                NULLIF(COUNT(DISTINCT o.order_id), 0),
                2
            ),
            0
        ) AS average_customer_order_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'cancelled';
""")

INVENTORY_RISK_QUERY = text("""
    WITH sales AS (
        SELECT
            oi.product_id,
            COALESCE(
                SUM(
                    CASE
                        WHEN o.status != 'cancelled'
                        THEN oi.quantity
                        ELSE 0
                    END
                ) / NULLIF(
                    GREATEST(
                        DATE_PART(
                            'day',
                            MAX(o.order_date) - MIN(o.order_date)
                        ),
                        1
                    ),
                    0
                ),
                0
            ) AS avg_daily_sales
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        GROUP BY oi.product_id
    )
    SELECT
        COUNT(*) AS total_products,

        COUNT(*) FILTER (
            WHERE i.current_stock <= i.reorder_level
        ) AS low_stock_products,

        COUNT(*) FILTER (
            WHERE i.current_stock = 0
        ) AS out_of_stock_products,

        COALESCE(SUM(i.current_stock), 0) AS total_units

    FROM inventory i;
""")

LOW_STOCK_PRODUCTS_QUERY = text("""
    SELECT
        i.product_id,
        p.product_name,
        p.category,
        i.current_stock,
        i.reorder_level
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    WHERE i.current_stock <= i.reorder_level
    ORDER BY i.current_stock ASC
    LIMIT 20;
""")

RETURNS_ANALYTICS_QUERY = text("""
    SELECT
        COUNT(*) AS total_returns,
        COALESCE(SUM(quantity), 0) AS returned_units,
        COALESCE(ROUND(SUM(refund_amount), 2), 0) AS total_refunds
    FROM returns;
""")

RETURN_REASONS_QUERY = text("""
    SELECT
        reason,
        COUNT(*) AS return_count,
        COALESCE(ROUND(SUM(refund_amount), 2), 0) AS refund_amount
    FROM returns
    GROUP BY reason
    ORDER BY return_count DESC;
""")

CATEGORY_PERFORMANCE_QUERY = text("""
    SELECT
        p.category,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
        ROUND(
            SUM(
                oi.quantity *
                (oi.unit_price - oi.unit_cost)
            ),
            2
        ) AS gross_profit
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY p.category
    ORDER BY revenue DESC;
""")
from sqlalchemy import text


SALES_TREND_QUERY = text("""
    SELECT
        DATE(order_date) AS date,
        COUNT(*) AS orders,
        COALESCE(ROUND(SUM(total_amount), 2), 0) AS revenue
    FROM orders
    WHERE status != 'cancelled'
    GROUP BY DATE(order_date)
    ORDER BY date;
""")
