import pandas as pd
from sklearn.ensemble import IsolationForest

from app.database.connection import engine


def get_daily_sales_data():
    query = """
        SELECT
            DATE(order_date) AS date,
            COUNT(*) AS orders,
            COALESCE(SUM(total_amount), 0) AS revenue
        FROM orders
        WHERE status != 'cancelled'
        GROUP BY DATE(order_date)
        ORDER BY date;
    """

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def detect_sales_anomalies():
    df = get_daily_sales_data()

    if len(df) < 20:
        return []

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(
        df[["orders", "revenue"]]
    )

    anomalies = df[df["anomaly"] == -1].copy()

    return [
        {
            "date": str(row["date"]),
            "orders": int(row["orders"]),
            "revenue": round(float(row["revenue"]), 2),
            "anomaly": "high"
        }
        for _, row in anomalies.iterrows()
    ]
