from app.database.connection import engine

from app.analytics.queries import (
    TOTAL_REVENUE_QUERY,
    ITEM_REVENUE_QUERY,
    ORDER_STATUS_QUERY,
    GROSS_PROFIT_QUERY,
    TOP_PRODUCTS_QUERY,
    ORDER_KPI_QUERY,
    PRODUCT_PERFORMANCE_QUERY,
    CUSTOMER_ANALYTICS_QUERY,
    CUSTOMER_ORDER_VALUE_QUERY,
    INVENTORY_RISK_QUERY,
    LOW_STOCK_PRODUCTS_QUERY,
    RETURNS_ANALYTICS_QUERY,
    RETURN_REASONS_QUERY,
    CATEGORY_PERFORMANCE_QUERY,
)


def get_total_revenue():
    with engine.connect() as connection:
        result = connection.execute(TOTAL_REVENUE_QUERY)
        row = result.mappings().one()
        return float(row["total_revenue"])



def get_item_revenue():
    with engine.connect() as connection:
        result = connection.execute(ITEM_REVENUE_QUERY)
        row = result.mappings().one()
        return float(row["item_revenue"])


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
        cancellation_rate = (
            (cancelled_orders / total_orders) * 100
            if total_orders > 0
            else 0
        )

        item_revenue = get_item_revenue()

        average_order_value = (
            item_revenue / active_orders
            if active_orders > 0
            else 0
        )

        return {
            "total_orders": total_orders,
            "active_orders": active_orders,
            "cancelled_orders": cancelled_orders,
            "cancellation_rate": round(cancellation_rate, 2),
            "average_order_value": round(average_order_value, 2),
        }


def get_product_performance():
    with engine.connect() as connection:
        result = connection.execute(PRODUCT_PERFORMANCE_QUERY)
        rows = result.mappings().all()

        return [
            {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "category": row["category"],
                "units_sold": int(row["units_sold"]),
                "revenue": float(row["revenue"]),
                "cost": float(row["cost"]),
                "gross_profit": float(row["gross_profit"]),
                "gross_margin": float(row["gross_margin"]),
            }
            for row in rows
        ]


def get_overview():
    total_revenue = get_item_revenue()
    estimated_gross_profit = get_estimated_gross_profit()
    order_status = get_order_status_metrics()
    order_kpis = get_order_kpis()
    top_products = get_top_products()

    gross_margin = (
        (estimated_gross_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
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

def get_customer_analytics():
    with engine.connect() as connection:
        result = connection.execute(CUSTOMER_ANALYTICS_QUERY)
        row = result.mappings().one()

        return {
            "total_customers": int(row["total_customers"]),
            "new_customers_90_days": int(row["new_customers"]),
        }


def get_customer_order_value():
    with engine.connect() as connection:
        result = connection.execute(CUSTOMER_ORDER_VALUE_QUERY)
        row = result.mappings().one()

        return float(row["average_customer_order_value"])


def get_inventory_risk():
    with engine.connect() as connection:
        result = connection.execute(INVENTORY_RISK_QUERY)
        row = result.mappings().one()

        return {
            "total_products": int(row["total_products"]),
            "low_stock_products": int(row["low_stock_products"]),
            "out_of_stock_products": int(row["out_of_stock_products"]),
            "total_units": int(row["total_units"]),
        }


def get_low_stock_products():
    with engine.connect() as connection:
        result = connection.execute(LOW_STOCK_PRODUCTS_QUERY)
        rows = result.mappings().all()

        return [
            {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "category": row["category"],
                "current_stock": int(row["current_stock"]),
                "reorder_level": int(row["reorder_level"]),
            }
            for row in rows
        ]


def get_returns_analytics():
    with engine.connect() as connection:
        result = connection.execute(RETURNS_ANALYTICS_QUERY)
        row = result.mappings().one()

        return {
            "total_returns": int(row["total_returns"]),
            "returned_units": int(row["returned_units"]),
            "total_refunds": float(row["total_refunds"]),
        }


def get_return_reasons():
    with engine.connect() as connection:
        result = connection.execute(RETURN_REASONS_QUERY)
        rows = result.mappings().all()

        return [
            {
                "reason": row["reason"],
                "return_count": int(row["return_count"]),
                "refund_amount": float(row["refund_amount"]),
            }
            for row in rows
        ]


def get_category_performance():
    with engine.connect() as connection:
        result = connection.execute(CATEGORY_PERFORMANCE_QUERY)
        rows = result.mappings().all()

        return [
            {
                "category": row["category"],
                "units_sold": int(row["units_sold"]),
                "revenue": float(row["revenue"]),
                "gross_profit": float(row["gross_profit"]),
            }
            for row in rows
        ]

def get_sales_trend():
    from app.analytics.queries import SALES_TREND_QUERY

    with engine.connect() as connection:
        result = connection.execute(SALES_TREND_QUERY)
        rows = result.mappings().all()

        return [
            {
                "date": str(row["date"]),
                "orders": int(row["orders"]),
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ]
