from fastapi import FastAPI

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