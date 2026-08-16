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
        total_units_sold_30_days = int(row["total_units_sold_30_days"])

        avg_daily_sales = total_units_sold_30_days / 30.0

        if avg_daily_sales > 0:
            estimated_days = current_stock / avg_daily_sales
        else:
            estimated_days = None

        # ----------------------------------------------------
        # RISK CLASSIFICATION
        # ----------------------------------------------------

        if current_stock == 0:
            risk = "critical"
            risk_score = 100

        elif estimated_days is not None and estimated_days <= 7:
            risk = "high"
            risk_score = max(
                75,
                min(99, round(100 - (estimated_days / 7) * 25))
            )

        elif estimated_days is not None and estimated_days <= 14:
            risk = "medium"
            risk_score = max(
                50,
                min(74, round(75 - ((estimated_days - 7) / 7) * 25))
            )

        elif current_stock <= reorder_level:
            risk = "medium"
            risk_score = 60

        else:
            risk = "low"

            if avg_daily_sales > 0 and estimated_days is not None:
                risk_score = max(
                    1,
                    min(49, round(50 - min(estimated_days, 50)))
                )
            else:
                risk_score = 5

        # ----------------------------------------------------
        # STOCK COVERAGE
        # ----------------------------------------------------

        if estimated_days is None:
            stock_coverage = "No sales velocity"
        elif estimated_days <= 7:
            stock_coverage = "Critical"
        elif estimated_days <= 14:
            stock_coverage = "Low"
        elif estimated_days <= 30:
            stock_coverage = "Healthy"
        else:
            stock_coverage = "Overstocked"

        # ----------------------------------------------------
        # REORDER RECOMMENDATION
        # Target = approximately 30 days of demand, but never
        # below the configured reorder level.
        # ----------------------------------------------------

        target_stock = max(
            reorder_level,
            round(avg_daily_sales * 30)
        )

        recommended_reorder_qty = max(
            0,
            target_stock - current_stock
        )

        if current_stock == 0:
            urgency = "Immediate"
        elif estimated_days is not None and estimated_days <= 7:
            urgency = "Within 7 days"
        elif current_stock <= reorder_level:
            urgency = "Reorder soon"
        else:
            urgency = "Monitor"

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
                "risk_score": int(risk_score),
                "stock_coverage": stock_coverage,
                "target_stock": int(target_stock),
                "recommended_reorder_qty": int(recommended_reorder_qty),
                "urgency": urgency,
            }
        )

    return results
