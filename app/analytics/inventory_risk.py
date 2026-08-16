from app.database.connection import engine
import pandas as pd


def get_inventory_risk():

    query = """
        WITH max_date AS (
            SELECT MAX(DATE(order_date)) AS latest_date
            FROM orders
            WHERE status != 'cancelled'
        ),
        sales AS (
            SELECT
                oi.product_id,
                COALESCE(SUM(oi.quantity), 0) AS total_units
            FROM order_items oi
            JOIN orders o
                ON oi.order_id = o.order_id
            CROSS JOIN max_date md
            WHERE o.status != 'cancelled'
              AND DATE(o.order_date) >= md.latest_date - INTERVAL '29 days'
              AND DATE(o.order_date) <= md.latest_date
            GROUP BY oi.product_id
        )
        SELECT
            i.product_id,
            p.product_name,
            p.category,
            i.current_stock,
            i.reorder_level,
            COALESCE(s.total_units, 0) AS total_units_sold_30_days
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        LEFT JOIN sales s
            ON i.product_id = s.product_id
        ORDER BY i.current_stock ASC;
    """

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    results = []

    for _, row in df.iterrows():

        current_stock = int(row["current_stock"])
        reorder_level = int(row["reorder_level"])

        total_units_sold_30_days = int(
            row["total_units_sold_30_days"]
        )

        # Exactly 30 calendar days.
        avg_daily_sales = total_units_sold_30_days / 30.0

        # If there are no sales, stockout cannot be estimated
        # from sales velocity.
        if avg_daily_sales > 0:
            estimated_days = current_stock / avg_daily_sales
        else:
            estimated_days = None

        # Risk classification
        if current_stock == 0:
            risk = "critical"

        elif estimated_days is not None and estimated_days <= 7:
            risk = "high"

        elif estimated_days is not None and estimated_days <= 14:
            risk = "medium"

        elif current_stock <= reorder_level:
            risk = "medium"

        else:
            risk = "low"

        results.append(
            {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "category": row["category"],
                "current_stock": current_stock,
                "reorder_level": reorder_level,
                "avg_daily_sales": round(avg_daily_sales, 2),
                "estimated_days_until_stockout": (
                    round(estimated_days, 1)
                    if estimated_days is not None
                    else None
                ),
                "risk": risk,
            }
        )

    return results