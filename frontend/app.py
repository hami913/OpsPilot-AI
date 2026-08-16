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
    page_icon="âš¡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       OPSPILOT AI - DARK PROFESSIONAL THEME
       ======================================================== */

    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    .main {
        background: #0f172a;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Titles */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc !important;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 17px;
        color: #94a3b8 !important;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #f8fafc !important;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #22c55e !important;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        background: #1e293b !important;
        border-radius: 12px !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    /* Buttons */
    .stButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* Selectbox */
    [data-baseweb="select"] > div {
        background: #1e293b !important;
        color: #f8fafc !important;
        border-color: #334155 !important;
    }

    /* Info / success / warning cards */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* General text */
    p, label, span, div {
        color: inherit;
    }

    /* Insight cards */
    .insight-card {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .insight-title {
        color: #f8fafc !important;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .insight-message {
        color: #cbd5e1 !important;
        font-size: 14px;
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
            âš¡ OpsPilot
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

    if st.button("ðŸ”„ Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(
        """
        <div style="margin-top:30px;font-size:12px;color:#9ca3af !important;">
            Backend<br>
            <span style="color:#22c55e !important;">â— Connected</span>
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
            icon = "ðŸ”´"
        elif priority == "HIGH":
            icon = "ðŸŸ "
        elif priority == "MEDIUM":
            icon = "ðŸŸ¡"
        else:
            icon = "ðŸŸ¢"

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    {icon} {insight["title"]}
                </div>
                <div style="color:#cbd5e1 !important;font-size:14px;line-height:1.6;">
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

    if sales_df.empty:
        st.warning("No sales trend data available.")
        st.stop()

    sales_df["date"] = pd.to_datetime(sales_df["date"])

    total_orders = overview["orders"]["total"]
    avg_order_value = overview["orders"]["average_order_value"]
    total_revenue = sales_df["revenue"].sum()
    peak_day = sales_df.loc[sales_df["revenue"].idxmax()]

    # --------------------------------------------------------
    # SALES KPI CARDS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Sales Performance</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Orders",
        f"{total_orders:,}",
    )

    c2.metric(
        "Average Order Value",
        f"${avg_order_value:,.2f}",
    )

    c3.metric(
        "Sales Revenue",
        f"${total_revenue:,.0f}",
    )

    c4.metric(
        "Peak Sales Day",
        f"${peak_day['revenue']:,.0f}",
    )

    st.write("")

    # --------------------------------------------------------
    # REVENUE TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Revenue Trend</div>',
        unsafe_allow_html=True,
    )

    revenue_chart = (
        alt.Chart(sales_df)
        .mark_line(point=True)
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
                alt.Tooltip(
                    "date:T",
                    title="Date",
                ),
                alt.Tooltip(
                    "orders:Q",
                    title="Orders",
                    format=",",
                ),
                alt.Tooltip(
                    "revenue:Q",
                    title="Revenue",
                    format=",.2f",
                ),
            ],
        )
        .properties(height=400)
        .interactive()
    )

    st.altair_chart(
        revenue_chart,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # ORDERS + REVENUE ANALYSIS
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Orders Trend</div>',
            unsafe_allow_html=True,
        )

        orders_chart = (
            alt.Chart(sales_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "date:T",
                    title="Date",
                ),
                y=alt.Y(
                    "orders:Q",
                    title="Orders",
                ),
                tooltip=[
                    alt.Tooltip(
                        "date:T",
                        title="Date",
                    ),
                    alt.Tooltip(
                        "orders:Q",
                        title="Orders",
                        format=",",
                    ),
                ],
            )
            .properties(height=320)
            .interactive()
        )

        st.altair_chart(
            orders_chart,
            use_container_width=True,
        )

    with right:

        st.markdown(
            '<div class="section-title">Order Status</div>',
            unsafe_allow_html=True,
        )

        status_df = pd.DataFrame(
            overview["orders"]["by_status"]
        )

        if not status_df.empty:

            status_chart = (
                alt.Chart(status_df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "count:Q",
                        title="Orders",
                    ),
                    y=alt.Y(
                        "status:N",
                        sort="-x",
                        title="Status",
                    ),
                    tooltip=[
                        "status",
                        alt.Tooltip(
                            "count:Q",
                            title="Orders",
                            format=",",
                        ),
                    ],
                )
                .properties(height=320)
            )

            st.altair_chart(
                status_chart,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # DAILY SALES TABLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Daily Sales Performance</div>',
        unsafe_allow_html=True,
    )

    display_df = sales_df.copy()

    display_df["date"] = display_df["date"].dt.strftime(
        "%Y-%m-%d"
    )

    display_df["revenue"] = display_df["revenue"].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# INVENTORY INTELLIGENCE
# ============================================================

elif page == "Inventory & Risk":

    st.markdown(
        '<div class="section-title">Inventory Intelligence</div>',
        unsafe_allow_html=True,
    )

    risk_df = pd.DataFrame(inventory_risk)

    if risk_df.empty:
        st.warning("No inventory risk data available.")
        st.stop()

    critical_df = risk_df[risk_df["risk"] == "critical"]
    high_df = risk_df[risk_df["risk"] == "high"]
    medium_df = risk_df[risk_df["risk"] == "medium"]
    low_df = risk_df[risk_df["risk"] == "low"]

    critical = len(critical_df)
    high = len(high_df)
    medium = len(medium_df)
    low = len(low_df)

    # --------------------------------------------------------
    # RISK KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Critical Risk", critical, "Immediate action")
    c2.metric("High Risk", high, "Priority action")
    c3.metric("Medium Risk", medium, "Monitor")
    c4.metric("Low Risk", low, "Healthy")

    st.write("")

    # --------------------------------------------------------
    # RISK DISTRIBUTION + SUMMARY
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Risk Distribution</div>',
            unsafe_allow_html=True,
        )

        risk_counts = pd.DataFrame(
            {
                "Risk": ["Critical", "High", "Medium", "Low"],
                "Products": [critical, high, medium, low],
            }
        )

        risk_chart = (
            alt.Chart(risk_counts)
            .mark_bar()
            .encode(
                x=alt.X("Products:Q", title="Products"),
                y=alt.Y(
                    "Risk:N",
                    sort=["Critical", "High", "Medium", "Low"],
                    title=None,
                ),
                tooltip=["Risk", "Products"],
            )
            .properties(height=300)
        )

        st.altair_chart(
            risk_chart,
            use_container_width=True,
        )

    with right:

        st.markdown(
            '<div class="section-title">Inventory Summary</div>',
            unsafe_allow_html=True,
        )

        inventory_summary = inventory["inventory"]

        s1, s2 = st.columns(2)

        s1.metric(
            "Total Products",
            f"{inventory_summary['total_products']:,}",
        )

        s2.metric(
            "Total Units",
            f"{inventory_summary['total_units']:,}",
        )

        s3, s4 = st.columns(2)

        s3.metric(
            "Low Stock",
            f"{inventory_summary['low_stock_products']:,}",
        )

        s4.metric(
            "Out of Stock",
            f"{inventory_summary['out_of_stock_products']:,}",
        )

        st.info(
            f"{critical} products require immediate attention "
            f"and {high} additional products have high stockout risk."
        )

    # --------------------------------------------------------
    # CRITICAL PRODUCTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">?? Immediate Action Required</div>',
        unsafe_allow_html=True,
    )

    critical_display = critical_df[
        [
            "product_name",
            "category",
            "current_stock",
            "reorder_level",
            "avg_daily_sales",
            "estimated_days_until_stockout",
            "risk",
        ]
    ].copy()

    if not critical_display.empty:

        critical_display = critical_display.sort_values(
            by="estimated_days_until_stockout"
        )

        critical_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Avg Daily Sales",
            "Days Until Stockout",
            "Risk",
        ]

        st.dataframe(
            critical_display,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.success("No critical inventory risks detected.")

    # --------------------------------------------------------
    # HIGH RISK PRODUCTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">?? High Risk Products</div>',
        unsafe_allow_html=True,
    )

    high_display = high_df[
        [
            "product_name",
            "category",
            "current_stock",
            "reorder_level",
            "avg_daily_sales",
            "estimated_days_until_stockout",
            "risk",
        ]
    ].copy()

    if not high_display.empty:

        high_display = high_display.sort_values(
            by="estimated_days_until_stockout"
        )

        high_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Avg Daily Sales",
            "Days Until Stockout",
            "Risk",
        ]

        st.dataframe(
            high_display,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.success("No high-risk products detected.")

    # --------------------------------------------------------
    # REORDER RECOMMENDATIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">?? Reorder Recommendations</div>',
        unsafe_allow_html=True,
    )

    reorder_df = risk_df[
        risk_df["current_stock"] <= risk_df["reorder_level"]
    ].copy()

    if not reorder_df.empty:

        reorder_df["recommended_order_qty"] = (
            reorder_df["reorder_level"]
            - reorder_df["current_stock"]
        )

        reorder_df = reorder_df.sort_values(
            by=["risk", "estimated_days_until_stockout"]
        )

        reorder_display = reorder_df[
            [
                "product_name",
                "category",
                "current_stock",
                "reorder_level",
                "recommended_order_qty",
                "risk",
            ]
        ].copy()

        reorder_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Recommended Reorder Qty",
            "Risk",
        ]

        st.dataframe(
            reorder_display,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Recommended reorder quantity is based on replenishing "
            "stock up to the configured reorder level."
        )

    else:
        st.success("No products currently require replenishment.")


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
# AI DECISION CENTER
# ============================================================

elif page == "AI Insights":

    st.markdown(
        '<div class="section-title">AI Decision Center</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Business priorities automatically generated from your operational data."
    )

    insights = intelligence["insights"]

    critical_insights = [
        x for x in insights
        if x["priority"].lower() == "critical"
    ]

    high_insights = [
        x for x in insights
        if x["priority"].lower() == "high"
    ]

    medium_insights = [
        x for x in insights
        if x["priority"].lower() == "medium"
    ]

    positive_insights = [
        x for x in insights
        if x["type"].lower() == "positive"
    ]

    # ========================================================
    # SUMMARY
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Critical Actions",
        len(critical_insights),
    )

    c2.metric(
        "High Priority",
        len(high_insights),
    )

    c3.metric(
        "Warnings",
        len(medium_insights),
    )

    c4.metric(
        "Positive Signals",
        len(positive_insights),
    )

    if critical_insights:
        st.warning(
            f"Immediate attention required: "
            f"{len(critical_insights)} critical business issues detected."
        )

    # ========================================================
    # HELPER
    # ========================================================

    def show_insight(insight):

        priority = insight["priority"].lower()

        title = insight["title"]
        area = insight["area"]
        message = insight["message"]

        if priority == "critical":

            st.error(
                f"CRITICAL — {title}\n\n"
                f"Area: {area}\n\n"
                f"{message}"
            )

        elif priority == "high":

            st.warning(
                f"HIGH PRIORITY — {title}\n\n"
                f"Area: {area}\n\n"
                f"{message}"
            )

        elif priority == "medium":

            st.info(
                f"WARNING — {title}\n\n"
                f"Area: {area}\n\n"
                f"{message}"
            )

        else:

            st.success(
                f"POSITIVE — {title}\n\n"
                f"Area: {area}\n\n"
                f"{message}"
            )

    # ========================================================
    # CRITICAL ACTIONS
    # ========================================================

    if critical_insights:

        st.markdown("### Critical Actions")

        for insight in critical_insights:
            show_insight(insight)

    # ========================================================
    # HIGH PRIORITY
    # ========================================================

    if high_insights:

        st.markdown("### High Priority")

        for insight in high_insights:
            show_insight(insight)

    # ========================================================
    # WARNINGS
    # ========================================================

    if medium_insights:

        st.markdown("### Business Warnings")

        for insight in medium_insights:
            show_insight(insight)

    # ========================================================
    # POSITIVE
    # ========================================================

    if positive_insights:

        st.markdown("### Positive Signals")

        for insight in positive_insights:
            show_insight(insight)

    # ========================================================
    # RECOMMENDED ACTIONS
    # ========================================================

    st.markdown("### Recommended Next Actions")

    summary = intelligence["summary"]

    actions = []

    if summary["out_of_stock_products"] > 0:

        actions.append(
            f"Replenish {summary['out_of_stock_products']:,} "
            "out-of-stock products immediately."
        )

    if summary["low_stock_products"] > 0:

        actions.append(
            f"Review {summary['low_stock_products']:,} "
            "products below their reorder level."
        )

    if summary["sales_anomalies"] > 0:

        actions.append(
            f"Investigate {summary['sales_anomalies']:,} "
            "detected sales anomalies."
        )

    if summary["total_returns"] > 0:

        actions.append(
            f"Review return drivers across "
            f"{summary['total_returns']:,} returns."
        )

    for index, action in enumerate(actions, 1):

        st.markdown(
            f"**{index}.** {action}"
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
        OpsPilot AI Â· Business Operations Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True,
)

