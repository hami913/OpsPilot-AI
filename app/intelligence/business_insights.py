from app.analytics.metrics import (
    get_overview,
    get_customer_analytics,
    get_inventory_risk,
    get_returns_analytics,
    get_category_performance,
)

from app.analytics.anomaly import detect_sales_anomalies
from app.analytics.inventory_risk import get_inventory_risk as get_detailed_inventory_risk


def generate_business_insights():

    overview = get_overview()
    customers = get_customer_analytics()
    inventory = get_inventory_risk()
    returns = get_returns_analytics()
    categories = get_category_performance()
    anomalies = detect_sales_anomalies()
    inventory_details = get_detailed_inventory_risk()

    insights = []

    # -----------------------------
    # ORDER / CANCELLATION
    # -----------------------------

    cancellation_rate = float(
        overview["orders"]["cancellation_rate"]
    )

    if cancellation_rate >= 5:
        insights.append({
            "type": "warning",
            "priority": "high",
            "area": "orders",
            "title": "High cancellation rate",
            "message": (
                f"Cancellation rate is {cancellation_rate:.2f}%. "
                "Investigate order cancellations and fulfillment issues."
            )
        })

    # -----------------------------
    # PROFIT
    # -----------------------------

    gross_margin = float(
        overview["profit"]["gross_margin"]
    )

    if gross_margin < 30:
        insights.append({
            "type": "warning",
            "priority": "high",
            "area": "profit",
            "title": "Low gross margin",
            "message": (
                f"Gross margin is {gross_margin:.2f}%. "
                "Review pricing and product costs."
            )
        })
    else:
        insights.append({
            "type": "positive",
            "priority": "low",
            "area": "profit",
            "title": "Healthy gross margin",
            "message": (
                f"Gross margin is currently {gross_margin:.2f}%."
            )
        })

    # -----------------------------
    # CUSTOMERS
    # -----------------------------

    total_customers = int(
        customers["total_customers"]
    )

    new_customers = int(
        customers["new_customers_90_days"]
    )

    if new_customers == 0:
        insights.append({
            "type": "warning",
            "priority": "high",
            "area": "customers",
            "title": "No recent customer acquisition",
            "message": (
                "No new customers were detected in the last 90 days. "
                "Check customer acquisition activity or tracking."
            )
        })

    # -----------------------------
    # INVENTORY
    # -----------------------------

    low_stock = int(
        inventory["low_stock_products"]
    )

    out_of_stock = int(
        inventory["out_of_stock_products"]
    )

    if out_of_stock > 0:
        insights.append({
            "type": "critical",
            "priority": "critical",
            "area": "inventory",
            "title": "Products out of stock",
            "message": (
                f"{out_of_stock} products have zero inventory. "
                "Immediate replenishment is recommended."
            )
        })

    if low_stock > 0:
        insights.append({
            "type": "warning",
            "priority": "medium",
            "area": "inventory",
            "title": "Low inventory detected",
            "message": (
                f"{low_stock} products are at or below reorder level."
            )
        })

    # -----------------------------
    # DETAILED INVENTORY RISK
    # -----------------------------

    critical = [
        item
        for item in inventory_details
        if item["risk"] == "critical"
    ]

    high = [
        item
        for item in inventory_details
        if item["risk"] == "high"
    ]

    if critical:
        insights.append({
            "type": "critical",
            "priority": "critical",
            "area": "inventory",
            "title": "Critical stockout risk",
            "message": (
                f"{len(critical)} products require immediate attention."
            )
        })

    if high:
        insights.append({
            "type": "warning",
            "priority": "high",
            "area": "inventory",
            "title": "High stockout risk",
            "message": (
                f"{len(high)} products have high stockout risk."
            )
        })

    # -----------------------------
    # RETURNS
    # -----------------------------

    total_returns = int(
        returns["total_returns"]
    )

    total_refunds = float(
        returns["total_refunds"]
    )

    if total_returns > 0:
        insights.append({
            "type": "warning",
            "priority": "medium",
            "area": "returns",
            "title": "Returns impacting revenue",
            "message": (
                f"{total_returns:,} returns generated "
                f"{total_refunds:,.2f} in refunds."
            )
        })

    # -----------------------------
    # CATEGORY
    # -----------------------------

    if categories:

        best_category = max(
            categories,
            key=lambda x: float(x["revenue"])
        )

        insights.append({
            "type": "positive",
            "priority": "low",
            "area": "products",
            "title": "Top performing category",
            "message": (
                f"{best_category['category']} is the "
                "top revenue-generating category."
            )
        })

    # -----------------------------
    # SALES ANOMALIES
    # -----------------------------

    if anomalies:
        insights.append({
            "type": "warning",
            "priority": "medium",
            "area": "sales",
            "title": "Sales anomalies detected",
            "message": (
                f"{len(anomalies)} unusual sales periods were detected."
            )
        })

    return {
        "summary": {
            "revenue": overview["revenue"]["total"],
            "gross_margin": overview["profit"]["gross_margin"],
            "total_customers": total_customers,
            "new_customers_90_days": new_customers,
            "low_stock_products": low_stock,
            "out_of_stock_products": out_of_stock,
            "total_returns": total_returns,
            "total_refunds": total_refunds,
            "sales_anomalies": len(anomalies),
        },
        "insights": insights,
    }
