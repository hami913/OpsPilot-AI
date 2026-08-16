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
