from fastapi import FastAPI

from app.analytics.metrics import (
    get_overview,
    get_product_performance,
    get_customer_analytics,
    get_customer_order_value,
    get_inventory_risk,
    get_low_stock_products,
    get_returns_analytics,
    get_return_reasons,
    get_category_performance,
    get_sales_trend,
)

from app.analytics.anomaly import detect_sales_anomalies
from app.intelligence.business_insights import generate_business_insights


app = FastAPI(
    title="OpsPilot AI",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "online",
        "project": "OpsPilot AI",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/analytics/overview")
def analytics_overview():
    return get_overview()


@app.get("/analytics/products")
def analytics_products():
    return get_product_performance()


@app.get("/analytics/customers")
def analytics_customers():
    return {
        "customers": get_customer_analytics(),
        "average_order_value": get_customer_order_value(),
    }



@app.get("/analytics/customer-intelligence")
def customer_intelligence():
    from app.database.connection import engine
    import pandas as pd

    with engine.connect() as connection:

        summary_query = """
            WITH customer_orders AS (
                SELECT
                    o.customer_id,
                    COUNT(DISTINCT o.order_id) AS order_count,
                    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status != 'cancelled'
                GROUP BY o.customer_id
            )
            SELECT
                COUNT(*) AS customers_with_orders,
                COUNT(*) FILTER (WHERE order_count >= 2) AS repeat_customers,
                COALESCE(AVG(order_count), 0) AS avg_orders_per_customer,
                COALESCE(AVG(revenue), 0) AS avg_customer_revenue,
                COALESCE(SUM(revenue), 0) AS customer_revenue
            FROM customer_orders;
        """

        top_query = """
            SELECT
                o.customer_id,
                COUNT(DISTINCT o.order_id) AS orders,
                COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
            FROM orders o
            JOIN order_items oi
                ON o.order_id = oi.order_id
            WHERE o.status != 'cancelled'
            GROUP BY o.customer_id
            ORDER BY revenue DESC
            LIMIT 10;
        """

        segment_query = """
            WITH customer_orders AS (
                SELECT
                    o.customer_id,
                    COUNT(DISTINCT o.order_id) AS order_count,
                    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status != 'cancelled'
                GROUP BY o.customer_id
            )
            SELECT
                CASE
                    WHEN order_count = 1 THEN 'One-time'
                    WHEN order_count BETWEEN 2 AND 4 THEN 'Repeat'
                    WHEN order_count >= 5 THEN 'Loyal'
                    ELSE 'Other'
                END AS segment,
                COUNT(*) AS customers,
                COALESCE(SUM(revenue), 0) AS revenue
            FROM customer_orders
            GROUP BY 1
            ORDER BY customers DESC;
        """

        summary = connection.execute(
            __import__("sqlalchemy").text(summary_query)
        ).mappings().first()

        top_df = pd.read_sql(top_query, connection)
        segment_df = pd.read_sql(segment_query, connection)

    total = int(summary["customers_with_orders"] or 0)
    repeat = int(summary["repeat_customers"] or 0)

    return {
        "customers_with_orders": total,
        "repeat_customers": repeat,
        "repeat_customer_rate": round(
            (repeat / total * 100) if total else 0,
            1,
        ),
        "avg_orders_per_customer": round(
            float(summary["avg_orders_per_customer"] or 0),
            2,
        ),
        "avg_customer_revenue": round(
            float(summary["avg_customer_revenue"] or 0),
            2,
        ),
        "customer_revenue": round(
            float(summary["customer_revenue"] or 0),
            2,
        ),
        "top_customers": top_df.to_dict(orient="records"),
        "segments": segment_df.to_dict(orient="records"),
    }

@app.get("/analytics/inventory")
def analytics_inventory():
    return {
        "inventory": get_inventory_risk(),
        "low_stock_products": get_low_stock_products(),
    }


@app.get("/analytics/returns")
def analytics_returns():
    return {
        "returns": get_returns_analytics(),
        "reasons": get_return_reasons(),
    }



@app.get("/analytics/returns-intelligence")
def returns_intelligence():
    from app.database.connection import engine
    import pandas as pd
    from sqlalchemy import text

    with engine.connect() as connection:

        summary_query = """
            WITH sales AS (
                SELECT
                    COALESCE(SUM(oi.quantity), 0) AS sold_units,
                    COALESCE(
                        SUM(oi.quantity * oi.unit_price),
                        0
                    ) AS sales_value
                FROM order_items oi
                JOIN orders o
                    ON oi.order_id = o.order_id
                WHERE o.status != 'cancelled'
            ),
            return_data AS (
                SELECT
                    COUNT(*) AS total_returns,
                    COALESCE(SUM(quantity), 0) AS returned_units,
                    COALESCE(SUM(refund_amount), 0) AS refunds
                FROM returns
            )
            SELECT
                s.sold_units,
                s.sales_value,
                r.total_returns,
                r.returned_units,
                r.refunds
            FROM sales s
            CROSS JOIN return_data r;
        """

        reason_query = """
            SELECT
                reason,
                COUNT(*) AS returns,
                COALESCE(SUM(quantity), 0) AS returned_units,
                COALESCE(SUM(refund_amount), 0) AS refunds
            FROM returns
            GROUP BY reason
            ORDER BY returns DESC;
        """

        monthly_query = """
            SELECT
                DATE_TRUNC('month', return_date) AS month,
                COUNT(*) AS returns,
                COALESCE(SUM(quantity), 0) AS returned_units,
                COALESCE(SUM(refund_amount), 0) AS refunds
            FROM returns
            GROUP BY DATE_TRUNC('month', return_date)
            ORDER BY month;
        """

        summary = connection.execute(
            text(summary_query)
        ).mappings().one()

        reason_df = pd.read_sql(
            text(reason_query),
            connection,
        )

        monthly_df = pd.read_sql(
            text(monthly_query),
            connection,
        )

    sold_units = int(summary["sold_units"] or 0)
    sales_value = float(summary["sales_value"] or 0)
    total_returns = int(summary["total_returns"] or 0)
    returned_units = int(summary["returned_units"] or 0)
    refunds = float(summary["refunds"] or 0)

    return_rate = (
        returned_units / sold_units * 100
        if sold_units
        else 0
    )

    refund_rate = (
        refunds / sales_value * 100
        if sales_value
        else 0
    )

    avg_refund = (
        refunds / total_returns
        if total_returns
        else 0
    )

    if return_rate >= 10:
        severity = "critical"
    elif return_rate >= 5:
        severity = "high"
    elif return_rate >= 2:
        severity = "medium"
    else:
        severity = "low"

    return {
        "sold_units": sold_units,
        "sales_value": round(sales_value, 2),
        "total_returns": total_returns,
        "returned_units": returned_units,
        "refunds": round(refunds, 2),
        "return_rate": round(return_rate, 2),
        "refund_rate": round(refund_rate, 2),
        "avg_refund_per_return": round(avg_refund, 2),
        "severity": severity,
        "reasons": reason_df.to_dict(orient="records"),
        "monthly": monthly_df.to_dict(orient="records"),
    }

@app.get("/analytics/categories")
def analytics_categories():
    return get_category_performance()


@app.get("/analytics/sales-trend")
def sales_trend():
    return get_sales_trend()


@app.get("/analytics/anomalies")
def sales_anomalies():
    return detect_sales_anomalies()


@app.get("/analytics/inventory-risk")
def inventory_risk():
    from app.analytics.inventory_risk import get_inventory_risk as get_detailed_inventory_risk
    return get_detailed_inventory_risk()


@app.get("/intelligence/insights")
def business_insights():
    return generate_business_insights()
