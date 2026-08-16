import requests
import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OpsPilot AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f7fb;
        }

        [data-testid="stSidebar"] {
            background: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #f9fafb !important;
        }

        .main-title {
            font-size: 34px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 4px;
        }

        .subtitle {
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 21px;
            font-weight: 750;
            color: #111827;
            margin-top: 18px;
            margin-bottom: 12px;
        }

        .insight-card {
            padding: 15px 17px;
            border-radius: 12px;
            background: white;
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
        }

        .insight-title {
            font-weight: 700;
            color: #111827;
            margin-bottom: 5px;
        }

        .insight-message {
            color: #4b5563;
            font-size: 14px;
        }

        .risk-critical {
            color: #b91c1c;
            font-weight: 800;
        }

        .risk-high {
            color: #c2410c;
            font-weight: 800;
        }

        .risk-medium {
            color: #a16207;
            font-weight: 800;
        }

        .risk-low {
            color: #15803d;
            font-weight: 800;
        }

        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
            margin-top: 35px;
            padding: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

@st.cache_data(ttl=60)
def get_api(endpoint):
    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def safe_api(endpoint):
    try:
        return get_api(endpoint), None
    except requests.exceptions.ConnectionError:
        return None, "FastAPI backend is not running."
    except requests.exceptions.Timeout:
        return None, f"Request timed out: {endpoint}"
    except requests.exceptions.HTTPError as exc:
        return None, f"API error: {exc}"
    except Exception as exc:
        return None, str(exc)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="font-size:28px;font-weight:800;margin-bottom:4px;">
            ⚡ OpsPilot
        </div>
        <div style="font-size:13px;color:#9ca3af !important;">
            AI Operations Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Sales Analytics",
            "Inventory & Risk",
            "Customers",
            "Returns",
            "AI Insights",
            "Anomalies",
        ],
    )

    st.divider()

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(
        """
        <div style="margin-top:30px;font-size:12px;color:#9ca3af !important;">
            Backend<br>
            <span style="color:#22c55e !important;">● Connected</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

overview, overview_error = safe_api("/analytics/overview")
customers, customers_error = safe_api("/analytics/customers")
inventory, inventory_error = safe_api("/analytics/inventory")
returns, returns_error = safe_api("/analytics/returns")
categories, categories_error = safe_api("/analytics/categories")
sales_trend, sales_error = safe_api("/analytics/sales-trend")
anomalies, anomalies_error = safe_api("/analytics/anomalies")
inventory_risk, risk_error = safe_api("/analytics/inventory-risk")
intelligence, intelligence_error = safe_api("/intelligence/insights")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">OpsPilot AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-Powered Business Operations Command Center</div>',
    unsafe_allow_html=True,
)


# ============================================================
# ERROR CHECK
# ============================================================

all_errors = [
    overview_error,
    customers_error,
    inventory_error,
    returns_error,
    categories_error,
    sales_error,
    anomalies_error,
    risk_error,
    intelligence_error,
]

errors = [error for error in all_errors if error]

if errors:
    st.error(
        "Unable to connect to one or more backend APIs. "
        "Make sure FastAPI is running on http://127.0.0.1:8000."
    )

    with st.expander("Technical details"):
        for error in errors:
            st.write(error)

    st.stop()


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    summary = intelligence["summary"]

    revenue = summary["revenue"]
    gross_margin = summary["gross_margin"]
    total_customers = summary["total_customers"]
    new_customers = summary["new_customers_90_days"]
    low_stock = summary["low_stock_products"]
    out_of_stock = summary["out_of_stock_products"]
    total_returns = summary["total_returns"]
    refunds = summary["total_refunds"]
    sales_anomaly_count = summary["sales_anomalies"]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Revenue",
        f"${revenue:,.0f}",
    )

    col2.metric(
        "Gross Margin",
        f"{gross_margin:.2f}%",
    )

    col3.metric(
        "Customers",
        f"{total_customers:,}",
        f"+{new_customers:,} / 90 days",
    )

    col4.metric(
        "Returns",
        f"{total_returns:,}",
        f"${refunds:,.0f} refunds",
    )

    st.write("")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Low Stock",
        f"{low_stock}",
    )

    col6.metric(
        "Out of Stock",
        f"{out_of_stock}",
    )

    col7.metric(
        "Sales Anomalies",
        f"{sales_anomaly_count}",
    )

    col8.metric(
        "Cancellation Rate",
        f"{overview['orders']['cancellation_rate']:.2f}%",
    )

    # --------------------------------------------------------
    # SALES TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Sales Performance</div>',
        unsafe_allow_html=True,
    )

    sales_df = pd.DataFrame(sales_trend)

    if not sales_df.empty:
        sales_df["date"] = pd.to_datetime(sales_df["date"])

        chart = (
            alt.Chart(sales_df)
            .mark_line(point=False)
            .encode(
                x=alt.X(
                    "date:T",
                    title="Date",
                    axis=alt.Axis(format="%b %Y"),
                ),
                y=alt.Y(
                    "revenue:Q",
                    title="Revenue",
                ),
                tooltip=[
                    alt.Tooltip("date:T", title="Date"),
                    alt.Tooltip("revenue:Q", title="Revenue", format=",.2f"),
                    alt.Tooltip("orders:Q", title="Orders"),
                ],
            )
            .properties(height=360)
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)

    # --------------------------------------------------------
    # CATEGORY + INVENTORY
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Revenue by Category</div>',
            unsafe_allow_html=True,
        )

        category_df = pd.DataFrame(categories)

        if not category_df.empty:
            category_chart = (
                alt.Chart(category_df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "revenue:Q",
                        title="Revenue",
                    ),
                    y=alt.Y(
                        "category:N",
                        sort="-x",
                        title="Category",
                    ),
                    tooltip=[
                        "category",
                        alt.Tooltip(
                            "revenue:Q",
                            title="Revenue",
                            format=",.2f",
                        ),
                        alt.Tooltip(
                            "gross_profit:Q",
                            title="Gross Profit",
                            format=",.2f",
                        ),
                    ],
                )
                .properties(height=300)
            )

            st.altair_chart(
                category_chart,
                use_container_width=True,
            )

    with right:

        st.markdown(
            '<div class="section-title">Inventory Risk</div>',
            unsafe_allow_html=True,
        )

        risk_df = pd.DataFrame(inventory_risk)

        risk_counts = (
            risk_df["risk"]
            .value_counts()
            .reindex(
                ["critical", "high", "medium", "low"],
                fill_value=0,
            )
            .reset_index()
        )

        risk_counts.columns = ["risk", "count"]

        risk_chart = (
            alt.Chart(risk_counts)
            .mark_bar()
            .encode(
                x=alt.X(
                    "count:Q",
                    title="Products",
                ),
                y=alt.Y(
                    "risk:N",
                    sort=["critical", "high", "medium", "low"],
                    title="Risk",
                ),
                tooltip=["risk", "count"],
            )
            .properties(height=300)
        )

        st.altair_chart(
            risk_chart,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # AI INSIGHTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">AI Business Insights</div>',
        unsafe_allow_html=True,
    )

    insights = intelligence["insights"]

    for insight in insights:

        priority = insight["priority"].upper()

        if priority == "CRITICAL":
            icon = "🔴"
        elif priority == "HIGH":
            icon = "🟠"
        elif priority == "MEDIUM":
            icon = "🟡"
        else:
            icon = "🟢"

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    {icon} {insight["title"]}
                </div>
                <div class="insight-message">
                    {insight["message"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Top Products</div>',
        unsafe_allow_html=True,
    )

    top_products = pd.DataFrame(
        overview["top_products"]
    )

    if not top_products.empty:
        display_products = top_products[
            [
                "product_name",
                "category",
                "units_sold",
                "revenue",
            ]
        ].copy()

        display_products["revenue"] = display_products[
            "revenue"
        ].map(lambda x: f"${x:,.2f}")

        display_products.columns = [
            "Product",
            "Category",
            "Units Sold",
            "Revenue",
        ]

        st.dataframe(
            display_products,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# SALES ANALYTICS
# ============================================================

elif page == "Sales Analytics":

    st.markdown(
        '<div class="section-title">Sales Analytics</div>',
        unsafe_allow_html=True,
    )

    sales_df = pd.DataFrame(sales_trend)
    sales_df["date"] = pd.to_datetime(sales_df["date"])

    st.metric(
        "Total Orders",
        f"{overview['orders']['total']:,}",
    )

    st.metric(
        "Average Order Value",
        f"${overview['orders']['average_order_value']:,.2f}",
    )

    chart = (
        alt.Chart(sales_df)
        .mark_line()
        .encode(
            x="date:T",
            y="revenue:Q",
            tooltip=[
                "date:T",
                "orders:Q",
                alt.Tooltip(
                    "revenue:Q",
                    format=",.2f",
                ),
            ],
        )
        .properties(height=450)
        .interactive()
    )

    st.altair_chart(
        chart,
        use_container_width=True,
    )

    st.markdown(
        '<div class="section-title">Order Status</div>',
        unsafe_allow_html=True,
    )

    status_df = pd.DataFrame(
        overview["orders"]["by_status"]
    )

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# INVENTORY
# ============================================================

elif page == "Inventory & Risk":

    st.markdown(
        '<div class="section-title">Inventory & Risk Management</div>',
        unsafe_allow_html=True,
    )

    risk_df = pd.DataFrame(inventory_risk)

    critical = len(
        risk_df[risk_df["risk"] == "critical"]
    )

    high = len(
        risk_df[risk_df["risk"] == "high"]
    )

    medium = len(
        risk_df[risk_df["risk"] == "medium"]
    )

    low = len(
        risk_df[risk_df["risk"] == "low"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Critical", critical)
    c2.metric("High", high)
    c3.metric("Medium", medium)
    c4.metric("Low", low)

    st.markdown(
        '<div class="section-title">Products Requiring Attention</div>',
        unsafe_allow_html=True,
    )

    priority_df = risk_df[
        risk_df["risk"].isin(
            ["critical", "high"]
        )
    ].copy()

    priority_df = priority_df.sort_values(
        by=[
            "risk",
            "estimated_days_until_stockout",
        ]
    )

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# CUSTOMERS
# ============================================================

elif page == "Customers":

    st.markdown(
        '<div class="section-title">Customer Analytics</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Customers",
        f"{customers['customers']['total_customers']:,}",
    )

    c2.metric(
        "New Customers / 90 Days",
        f"{customers['customers']['new_customers_90_days']:,}",
    )

    c3.metric(
        "Average Order Value",
        f"${customers['average_order_value']:,.2f}",
    )


# ============================================================
# RETURNS
# ============================================================

elif page == "Returns":

    st.markdown(
        '<div class="section-title">Returns Analytics</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Returns",
        f"{returns['returns']['total_returns']:,}",
    )

    c2.metric(
        "Returned Units",
        f"{returns['returns']['returned_units']:,}",
    )

    c3.metric(
        "Refunds",
        f"${returns['returns']['total_refunds']:,.2f}",
    )

    reason_df = pd.DataFrame(
        returns["reasons"]
    )

    st.dataframe(
        reason_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# AI INSIGHTS
# ============================================================

elif page == "AI Insights":

    st.markdown(
        '<div class="section-title">AI Business Intelligence</div>',
        unsafe_allow_html=True,
    )

    for insight in intelligence["insights"]:

        priority = insight["priority"].upper()

        if priority == "CRITICAL":
            icon = "🔴"
        elif priority == "HIGH":
            icon = "🟠"
        elif priority == "MEDIUM":
            icon = "🟡"
        else:
            icon = "🟢"

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    {icon} {insight["title"]}
                </div>
                <div class="insight-message">
                    <b>Area:</b> {insight["area"]}<br>
                    <b>Priority:</b> {priority}<br><br>
                    {insight["message"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ANOMALIES
# ============================================================

elif page == "Anomalies":

    st.markdown(
        '<div class="section-title">Sales Anomaly Detection</div>',
        unsafe_allow_html=True,
    )

    anomaly_df = pd.DataFrame(anomalies)

    st.metric(
        "Detected Anomalies",
        len(anomaly_df),
    )

    if not anomaly_df.empty:

        anomaly_chart = (
            alt.Chart(anomaly_df)
            .mark_circle(size=100)
            .encode(
                x=alt.X(
                    "date:T",
                    title="Date",
                ),
                y=alt.Y(
                    "revenue:Q",
                    title="Revenue",
                ),
                tooltip=[
                    "date:T",
                    "orders:Q",
                    alt.Tooltip(
                        "revenue:Q",
                        format=",.2f",
                    ),
                    "anomaly",
                ],
            )
            .properties(height=400)
            .interactive()
        )

        st.altair_chart(
            anomaly_chart,
            use_container_width=True,
        )

        st.dataframe(
            anomaly_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OpsPilot AI · Business Operations Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True,
)