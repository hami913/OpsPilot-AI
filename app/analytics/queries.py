from sqlalchemy import text


TOTAL_REVENUE_QUERY = text("""
    SELECT
        COALESCE(ROUND(SUM(total_amount), 2), 0) AS total_revenue
    FROM orders
    WHERE status != 'cancelled';
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
