from fastapi import FastAPI

from app.analytics.metrics import (
    get_overview,
    get_product_performance,
)

app = FastAPI(
    title="OpsPilot AI",
    description="AI Operations Agent for E-commerce SMEs",
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
    return {
        "status": "healthy"
    }


@app.get("/analytics/overview")
def analytics_overview():
    return get_overview()


@app.get("/analytics/products")
def analytics_products():
    return {
        "products": get_product_performance()
    }
