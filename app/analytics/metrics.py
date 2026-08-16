from app.database.connection import engine

from app.analytics.queries import (
    TOTAL_REVENUE_QUERY,
    ORDER_STATUS_QUERY,
    GROSS_PROFIT_QUERY,
    TOP_PRODUCTS_QUERY,
)


def get_total_revenue():
    with engine.connect() as connection:
        result = connection.execute(TOTAL_REVENUE_QUERY)
        row = result.mappings().one()
        return float(row["total_revenue"])


def get_order_status_metrics():
    with engine.connect() as connection:
        result = connection.execute(ORDER_STATUS_QUERY)
        return [dict(row) for row in result.mappings().all()]


def get_estimated_gross_profit():
    with engine.connect() as connection:
        result = connection.execute(GROSS_PROFIT_QUERY)
        row = result.mappings().one()
        return float(row["estimated_gross_profit"])


def get_top_products():
    with engine.connect() as connection:
        result = connection.execute(TOP_PRODUCTS_QUERY)
        return [dict(row) for row in result.mappings().all()]


def get_overview():
    total_revenue = get_total_revenue()
    estimated_gross_profit = get_estimated_gross_profit()
    order_status = get_order_status_metrics()
    top_products = get_top_products()

    total_orders = sum(item["order_count"] for item in order_status)

    return {
        "revenue": {
            "total": total_revenue,
        },
        "profit": {
            "estimated_gross_profit": estimated_gross_profit,
        },
        "orders": {
            "total": total_orders,
            "by_status": order_status,
        },
        "top_products": top_products,
    }
