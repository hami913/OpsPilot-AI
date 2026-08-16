
from app.database.connection import engine
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np


def detect_sales_anomalies():

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
        df = pd.read_sql(query, connection)

    if df.empty or len(df) < 10:
        return []

    df["orders"] = df["orders"].astype(float)
    df["revenue"] = df["revenue"].astype(float)

    df["avg_order_value"] = np.where(
        df["orders"] > 0,
        df["revenue"] / df["orders"],
        0,
    )

    features = df[
        ["orders", "revenue", "avg_order_value"]
    ].fillna(0)

    model = IsolationForest(
        contamination=0.05,
        random_state=42,
    )

    df["anomaly_prediction"] = model.fit_predict(features)
    df["raw_score"] = model.decision_function(features)

    # Historical baselines
    order_mean = df["orders"].mean()
    revenue_mean = df["revenue"].mean()

    order_std = df["orders"].std()
    revenue_std = df["revenue"].std()

    if order_std == 0:
        order_std = 1

    if revenue_std == 0:
        revenue_std = 1

    anomalies = df[
        df["anomaly_prediction"] == -1
    ].copy()

    results = []

    for _, row in anomalies.iterrows():

        order_deviation = (
            (row["orders"] - order_mean)
            / order_mean
            * 100
            if order_mean
            else 0
        )

        revenue_deviation = (
            (row["revenue"] - revenue_mean)
            / revenue_mean
            * 100
            if revenue_mean
            else 0
        )

        order_z = abs(
            (row["orders"] - order_mean)
            / order_std
        )

        revenue_z = abs(
            (row["revenue"] - revenue_mean)
            / revenue_std
        )

        combined_z = max(
            order_z,
            revenue_z,
        )

        if combined_z >= 3:
            severity = "critical"
        elif combined_z >= 2:
            severity = "high"
        else:
            severity = "medium"

        if revenue_deviation >= 0:
            direction = "spike"
        else:
            direction = "drop"

        if (
            abs(revenue_deviation)
            >= abs(order_deviation) + 10
        ):
            reason = "Revenue changed significantly beyond normal order-volume movement."

        elif (
            abs(order_deviation)
            >= abs(revenue_deviation) + 10
        ):
            reason = "Order volume changed significantly compared with the normal baseline."

        else:
            reason = "Both order volume and revenue moved outside the normal operating range."

        if direction == "spike":
            impact = "Potential demand surge or unusually strong sales activity."
        else:
            impact = "Potential demand slowdown or sales performance deterioration."

        # Normalize Isolation Forest score to a readable 0-100 risk score.
        anomaly_score = max(
            0,
            min(
                100,
                round(
                    (1 - row["raw_score"]) * 100,
                    1,
                ),
            ),
        )

        results.append(
            {
                "date": str(row["date"]),
                "orders": int(row["orders"]),
                "revenue": round(float(row["revenue"]), 2),
                "avg_order_value": round(
                    float(row["avg_order_value"]),
                    2,
                ),
                "anomaly": "high",
                "severity": severity,
                "direction": direction,
                "anomaly_score": anomaly_score,
                "order_deviation_pct": round(
                    float(order_deviation),
                    2,
                ),
                "revenue_deviation_pct": round(
                    float(revenue_deviation),
                    2,
                ),
                "reason": reason,
                "business_impact": impact,
            }
        )

    return results
