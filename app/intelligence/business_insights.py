from app.analytics.metrics import (
    get_overview,
    get_customer_analytics,
    get_inventory_risk,
    get_returns_analytics,
    get_category_performance,
)

from app.analytics.anomaly import detect_sales_anomalies
from app.analytics.inventory_risk import get_inventory_risk as get_detailed_inventory_risk



def enrich_insights(insights):
    recommendations = {
        "High cancellation rate": (
            "Review cancellation reasons, fulfillment delays, payment failures, and inventory availability.",
            "Investigate the highest-volume cancellation causes and prioritize the top operational issue.",
            "Reducing cancellations can recover lost orders and improve fulfillment reliability."
        ),
        "Low gross margin": (
            "Review product-level margins, supplier costs, discounts, and pricing strategy.",
            "Identify the lowest-margin products and evaluate repricing or cost reduction opportunities.",
            "Margin improvement directly increases profitability without requiring additional order volume."
        ),
        "Healthy gross margin": (
            "Maintain pricing discipline while monitoring product-level margin changes.",
            "Track margin trends and investigate significant deterioration early.",
            "Stable margins support predictable profitability and sustainable growth."
        ),
        "No recent customer acquisition": (
            "Review acquisition channels, campaign performance, and customer tracking.",
            "Validate acquisition tracking and identify channels capable of generating new customers.",
            "Weak acquisition can reduce future revenue growth and customer lifetime value."
        ),
        "Products out of stock": (
            "Replenish zero-stock products immediately and review supplier lead times.",
            "Prioritize products with active demand and place replenishment orders.",
            "Stockouts can cause missed sales and reduce customer satisfaction."
        ),
        "Low inventory detected": (
            "Review products approaching their reorder levels and replenish according to demand.",
            "Prioritize low-stock products by sales velocity and reorder urgency.",
            "Early replenishment reduces the probability of future stockouts and lost revenue."
        ),
        "Critical stockout risk": (
            "Immediately replenish products classified as critical stockout risk.",
            "Prioritize critical products using recommended reorder quantities and urgency.",
            "Critical stockouts represent an immediate risk of lost sales."
        ),
        "High stockout risk": (
            "Review high-risk products and schedule replenishment before inventory reaches zero.",
            "Prioritize high-risk products based on demand velocity and remaining stock coverage.",
            "Proactive replenishment can prevent avoidable revenue loss."
        ),
        "Returns impacting revenue": (
            "Analyze return reasons, refund exposure, product quality, and fulfillment issues.",
            "Prioritize the return reasons generating the highest volume and refund amount.",
            "Reducing avoidable returns can lower refund costs and protect revenue."
        ),
        "Top performing category": (
            "Continue monitoring demand and inventory availability for the leading category.",
            "Protect inventory levels and evaluate opportunities to expand successful products.",
            "Strong categories can provide opportunities for additional revenue growth."
        ),
        "Sales anomalies detected": (
            "Investigate unusual sales periods and determine whether they represent demand changes or operational issues.",
            "Review the highest-severity anomalies first and compare them with promotions, inventory, and fulfillment events.",
            "Early anomaly investigation can prevent operational problems from becoming larger business impacts."
        ),
    }

    for insight in insights:
        title = insight.get("title", "")
        recommendation, action, impact = recommendations.get(
            title,
            (
                "Review the underlying operational data and monitor this area.",
                "Investigate the issue and prioritize corrective action based on business impact.",
                "Addressing the issue can improve operational performance and reduce business risk."
            )
        )

        insight["recommendation"] = recommendation
        insight["action"] = action
        insight["business_impact"] = impact

    return insights
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

    insights = enrich_insights(insights)

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
