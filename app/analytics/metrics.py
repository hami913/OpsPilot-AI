from app.database.connection import engine

from app.analytics.queries import (
    TOTAL_REVENUE_QUERY,
    ORDER_STATUS_QUERY,
    GROSS_PROFIT_QUERY,
    TOP_PRODUCTS_QUERY,
    ORDER_KPI_QUERY,
)


def get_total_revenue():
    with engine.connect() as connection:
        result = connection.execute(TOTAL_REVENUE_QUERY)
        row = result.mappings().one()
        return float(row["total_revenue"])


def get_order_status_metrics():
    with engine.connect() as connection:
        result = connection.execute(ORDER_STATUS_QUERY)
        rows = result.mappings().all()

        return [
            {
                "status": row["status"],
                "order_count": int(row["order_count"]),
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ]


def get_estimated_gross_profit():
    with engine.connect() as connection:
        result = connection.execute(GROSS_PROFIT_QUERY)
        row = result.mappings().one()
        return float(row["estimated_gross_profit"])


def get_top_products():
    with engine.connect() as connection:
        result = connection.execute(TOP_PRODUCTS_QUERY)
        rows = result.mappings().all()

        return [
            {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "category": row["category"],
                "units_sold": int(row["units_sold"]),
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ]


def get_order_kpis():
    with engine.connect() as connection:
        result = connection.execute(ORDER_KPI_QUERY)
        row = result.mappings().one()

        total_orders = int(row["total_orders"])
        active_orders = int(row["active_orders"])
        cancelled_orders = int(row["cancelled_orders"])
        total_revenue = float(row["total_revenue"])

        cancellation_rate = (
            (cancelled_orders / total_orders) * 100
            if total_orders > 0
            else 0.0
        )

        average_order_value = (
            total_revenue / active_orders
            if active_orders > 0
            else 0.0
        )

        return {
            "total_orders": total_orders,
            "active_orders": active_orders,
            "cancelled_orders": cancelled_orders,
            "cancellation_rate": round(cancellation_rate, 2),
            "average_order_value": round(average_order_value, 2),
            "total_revenue": total_revenue,
        }


def get_overview():
    total_revenue = get_total_revenue()
    estimated_gross_profit = get_estimated_gross_profit()
    order_status = get_order_status_metrics()
    top_products = get_top_products()
    order_kpis = get_order_kpis()

    gross_margin = (
        (estimated_gross_profit / total_revenue) * 100
        if total_revenue > 0
        else 0.0
    )

    return {
        "revenue": {
            "total": total_revenue,
        },
        "profit": {
            "estimated_gross_profit": estimated_gross_profit,
            "gross_margin": round(gross_margin, 2),
        },
        "orders": {
            "total": order_kpis["total_orders"],
            "active": order_kpis["active_orders"],
            "cancelled": order_kpis["cancelled_orders"],
            "cancellation_rate": order_kpis["cancellation_rate"],
            "average_order_value": order_kpis["average_order_value"],
            "by_status": order_status,
        },
        "top_products": top_products,
    }
