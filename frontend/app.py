import requests
import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="OpsPilot AI",
    page_icon="*",
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
            [+] OpsPilot
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
            <span style="color:#22c55e !important;">[+] Connected</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

overview, overview_error = safe_api("/analytics/overview")
customers, customers_error = safe_api("/analytics/customers")
customer_intelligence, customer_intelligence_error = safe_api("/analytics/customer-intelligence")
inventory, inventory_error = safe_api("/analytics/inventory")
returns, returns_error = safe_api("/analytics/returns")
returns_intelligence, returns_intelligence_error = safe_api("/analytics/returns-intelligence")
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
    customer_intelligence_error,
    inventory_error,
    returns_error,
    returns_intelligence_error,
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
        "Make sure FastAPI is running on http://127.0.0.1:8001."
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
        '<div class="section-title">Inventory Risk Command Center</div>',
        unsafe_allow_html=True,
    )

    risk_df = pd.DataFrame(inventory_risk)

    if risk_df.empty:
        st.warning("No inventory risk data available.")
        st.stop()

    # --------------------------------------------------------
    # RISK SEGMENTS
    # --------------------------------------------------------

    critical_df = risk_df[risk_df["risk"] == "critical"].copy()
    high_df = risk_df[risk_df["risk"] == "high"].copy()
    medium_df = risk_df[risk_df["risk"] == "medium"].copy()
    low_df = risk_df[risk_df["risk"] == "low"].copy()

    critical = len(critical_df)
    high = len(high_df)
    medium = len(medium_df)
    low = len(low_df)

    total_products = len(risk_df)
    risk_products = critical + high + medium

    reorder_df = risk_df[
        risk_df["current_stock"] <= risk_df["reorder_level"]
    ].copy()

    total_reorder_units = int(
        reorder_df["recommended_reorder_qty"].sum()
    ) if not reorder_df.empty else 0

    avg_risk_score = round(
        risk_df["risk_score"].mean(),
        1
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Critical Risk",
        f"{critical:,}",
        "Immediate action",
    )

    c2.metric(
        "High Risk",
        f"{high:,}",
        "Priority action",
    )

    c3.metric(
        "Products at Risk",
        f"{risk_products:,}",
        f"{(risk_products / total_products * 100):.1f}% of inventory",
    )

    c4.metric(
        "Risk Score",
        f"{avg_risk_score:.1f}/100",
        "Higher = more risk",
    )

    st.write("")

    # --------------------------------------------------------
    # RISK DISTRIBUTION + INVENTORY SUMMARY
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
                tooltip=[
                    alt.Tooltip("Risk:N"),
                    alt.Tooltip("Products:Q"),
                ],
            )
            .properties(height=300)
        )

        st.altair_chart(
            risk_chart,
            use_container_width=True,
        )

    with right:

        st.markdown(
            '<div class="section-title">Inventory Health</div>',
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
            f"{critical} products are critical, "
            f"{high} are high risk, and "
            f"{total_reorder_units:,} units are recommended for reorder."
        )

    # --------------------------------------------------------
    # IMMEDIATE ACTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Immediate Action Required</div>',
        unsafe_allow_html=True,
    )

    critical_display = critical_df[
        [
            "product_name",
            "category",
            "current_stock",
            "avg_daily_sales",
            "estimated_days_until_stockout",
            "risk_score",
            "urgency",
        ]
    ].copy()

    if not critical_display.empty:

        critical_display = critical_display.sort_values(
            by="estimated_days_until_stockout",
            na_position="first",
        )

        critical_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Avg Daily Sales",
            "Days Until Stockout",
            "Risk Score",
            "Urgency",
        ]

        st.dataframe(
            critical_display,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.success("No critical inventory risks detected.")

    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">High Risk Products</div>',
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
            "risk_score",
            "urgency",
        ]
    ].copy()

    if not high_display.empty:

        high_display = high_display.sort_values(
            by="estimated_days_until_stockout",
            na_position="first",
        )

        high_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Avg Daily Sales",
            "Days Until Stockout",
            "Risk Score",
            "Urgency",
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
        '<div class="section-title">Reorder Recommendations</div>',
        unsafe_allow_html=True,
    )

    if not reorder_df.empty:

        reorder_display = reorder_df[
            [
                "product_name",
                "category",
                "current_stock",
                "reorder_level",
                "avg_daily_sales",
                "target_stock",
                "recommended_reorder_qty",
                "urgency",
            ]
        ].copy()

        reorder_display = reorder_display.sort_values(
            by="recommended_reorder_qty",
            ascending=False,
        )

        reorder_display.columns = [
            "Product",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Avg Daily Sales",
            "Target Stock",
            "Recommended Qty",
            "Urgency",
        ]

        st.dataframe(
            reorder_display,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.success("No products currently require replenishment.")

    # --------------------------------------------------------
    # CATEGORY RISK
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Category Risk Overview</div>',
        unsafe_allow_html=True,
    )

    category_risk = (
        risk_df.groupby("category")
        .agg(
            Products=("product_id", "count"),
            Critical=("risk", lambda x: (x == "critical").sum()),
            High=("risk", lambda x: (x == "high").sum()),
            Medium=("risk", lambda x: (x == "medium").sum()),
            Avg_Risk_Score=("risk_score", "mean"),
            Recommended_Reorder=("recommended_reorder_qty", "sum"),
        )
        .reset_index()
    )

    category_risk["Avg_Risk_Score"] = (
        category_risk["Avg_Risk_Score"].round(1)
    )

    category_risk = category_risk.sort_values(
        by="Avg_Risk_Score",
        ascending=False,
    )

    category_risk.columns = [
        "Category",
        "Products",
        "Critical",
        "High",
        "Medium",
        "Avg Risk Score",
        "Recommended Reorder",
    ]

    st.dataframe(
        category_risk,
        use_container_width=True,
        hide_index=True,
    )

elif page == "Customers":

    st.markdown(
        '<div class="section-title">Customer Intelligence</div>',
        unsafe_allow_html=True,
    )

    ci = customer_intelligence

    total_customers = customers["customers"]["total_customers"]
    new_customers = customers["customers"]["new_customers_90_days"]
    aov = customers["average_order_value"]

    active_customers = ci["customers_with_orders"]
    repeat_customers = ci["repeat_customers"]
    repeat_rate = ci["repeat_customer_rate"]
    avg_orders = ci["avg_orders_per_customer"]
    customer_revenue = ci["customer_revenue"]

    # --------------------------------------------------------
    # CUSTOMER KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Customers",
        f"{total_customers:,}",
    )

    c2.metric(
        "Active Customers",
        f"{active_customers:,}",
    )

    c3.metric(
        "New / 90 Days",
        f"{new_customers:,}",
    )

    c4.metric(
        "Average Order Value",
        f"${aov:,.2f}",
    )

    st.write("")

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Repeat Customers",
        f"{repeat_customers:,}",
    )

    c6.metric(
        "Repeat Rate",
        f"{repeat_rate:.1f}%",
    )

    c7.metric(
        "Avg Orders / Customer",
        f"{avg_orders:.2f}",
    )

    c8.metric(
        "Customer Revenue",
        f"${customer_revenue:,.0f}",
    )

    # --------------------------------------------------------
    # CUSTOMER SEGMENTS
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Customer Segments</div>',
            unsafe_allow_html=True,
        )

        segment_df = pd.DataFrame(ci["segments"])

        if not segment_df.empty:

            segment_chart = (
                alt.Chart(segment_df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "customers:Q",
                        title="Customers",
                    ),
                    y=alt.Y(
                        "segment:N",
                        sort="-x",
                        title=None,
                    ),
                    tooltip=[
                        "segment",
                        "customers",
                        "revenue",
                    ],
                )
                .properties(height=300)
            )

            st.altair_chart(
                segment_chart,
                use_container_width=True,
            )

    with right:

        st.markdown(
            '<div class="section-title">Customer Health</div>',
            unsafe_allow_html=True,
        )

        if repeat_rate >= 40:
            st.success(
                f"Strong customer retention signal: "
                f"{repeat_rate:.1f}% of active customers are repeat buyers."
            )
        elif repeat_rate >= 20:
            st.info(
                f"Moderate repeat behavior: "
                f"{repeat_rate:.1f}% of active customers are repeat buyers."
            )
        else:
            st.warning(
                f"Low repeat behavior detected: "
                f"only {repeat_rate:.1f}% of active customers are repeat buyers."
            )

        st.metric(
            "Average Revenue / Customer",
            f"${ci['avg_customer_revenue']:,.2f}",
        )

    # --------------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Top Customers by Revenue</div>',
        unsafe_allow_html=True,
    )

    top_df = pd.DataFrame(ci["top_customers"])

    if not top_df.empty:

        top_df = top_df.copy()

        top_df.insert(
            0,
            "Rank",
            range(1, len(top_df) + 1),
        )

        top_df["revenue"] = top_df["revenue"].round(2)

        top_df.columns = [
            "Rank",
            "Customer ID",
            "Orders",
            "Revenue",
        ]

        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No customer transaction data available.")


# ============================================================
# RETURNS
# ============================================================

elif page == "Returns":

    st.markdown(
        '<div class="section-title">Returns Intelligence</div>',
        unsafe_allow_html=True,
    )

    ri = returns_intelligence

    total_returns = ri["total_returns"]
    returned_units = ri["returned_units"]
    refunds = ri["refunds"]
    return_rate = ri["return_rate"]
    refund_rate = ri["refund_rate"]
    avg_refund = ri["avg_refund_per_return"]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Returns",
        f"{total_returns:,}",
    )

    c2.metric(
        "Returned Units",
        f"{returned_units:,}",
    )

    c3.metric(
        "Return Rate",
        f"{return_rate:.2f}%",
    )

    c4.metric(
        "Refunds",
        f"${refunds:,.0f}",
    )

    st.write("")

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Refund Rate",
        f"{refund_rate:.2f}%",
    )

    c6.metric(
        "Avg Refund / Return",
        f"${avg_refund:,.2f}",
    )

    c7.metric(
        "Units Sold",
        f"{ri['sold_units']:,}",
    )

    c8.metric(
        "Return Severity",
        ri["severity"].upper(),
    )

    # --------------------------------------------------------
    # BUSINESS HEALTH
    # --------------------------------------------------------

    severity = ri["severity"]

    if severity == "critical":
        st.error(
            f"Critical return pressure detected. "
            f"Return rate is {return_rate:.2f}%."
        )
    elif severity == "high":
        st.warning(
            f"High return pressure detected. "
            f"Return rate is {return_rate:.2f}%."
        )
    elif severity == "medium":
        st.info(
            f"Moderate return activity detected. "
            f"Return rate is {return_rate:.2f}%."
        )
    else:
        st.success(
            f"Return performance is healthy at "
            f"{return_rate:.2f}%."
        )

    # --------------------------------------------------------
    # RETURN REASONS
    # --------------------------------------------------------

    left, right = st.columns(2)

    reason_df = pd.DataFrame(
        ri["reasons"]
    )

    with left:

        st.markdown(
            '<div class="section-title">Return Reasons</div>',
            unsafe_allow_html=True,
        )

        if not reason_df.empty:

            reason_chart = (
                alt.Chart(reason_df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "returns:Q",
                        title="Returns",
                    ),
                    y=alt.Y(
                        "reason:N",
                        sort="-x",
                        title=None,
                    ),
                    tooltip=[
                        "reason",
                        "returns",
                        "returned_units",
                        "refunds",
                    ],
                )
                .properties(height=320)
            )

            st.altair_chart(
                reason_chart,
                use_container_width=True,
            )

    with right:

        st.markdown(
            '<div class="section-title">Reason Impact</div>',
            unsafe_allow_html=True,
        )

        if not reason_df.empty:

            reason_display = reason_df.copy()

            reason_display["refunds"] = (
                reason_display["refunds"].round(2)
            )

            reason_display.columns = [
                "Reason",
                "Returns",
                "Returned Units",
                "Refunds",
            ]

            st.dataframe(
                reason_display,
                use_container_width=True,
                hide_index=True,
            )

    # --------------------------------------------------------
    # MONTHLY RETURN TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Return Trend</div>',
        unsafe_allow_html=True,
    )

    monthly_df = pd.DataFrame(
        ri["monthly"]
    )

    if not monthly_df.empty:

        monthly_df["month"] = pd.to_datetime(
            monthly_df["month"]
        )

        trend_chart = (
            alt.Chart(monthly_df)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "month:T",
                    title="Month",
                ),
                y=alt.Y(
                    "returns:Q",
                    title="Returns",
                ),
                tooltip=[
                    "month",
                    "returns",
                    "returned_units",
                    "refunds",
                ],
            )
            .properties(height=320)
        )

        st.altair_chart(
            trend_chart,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RETURN DETAILS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Return Impact Analysis</div>',
        unsafe_allow_html=True,
    )

    impact1, impact2, impact3 = st.columns(3)

    impact1.metric(
        "Revenue at Risk",
        f"${refunds:,.2f}",
    )

    impact2.metric(
        "Refund / Return",
        f"${avg_refund:,.2f}",
    )

    impact3.metric(
        "Returned Unit Share",
        f"{return_rate:.2f}%",
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
        '<div class="section-title">Sales Anomaly Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "AI-powered detection of unusual sales behavior, revenue movements, and demand changes."
    )

    anomaly_df = pd.DataFrame(anomalies)

    if anomaly_df.empty:
        st.success("No significant sales anomalies detected.")
        st.stop()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    critical_count = int(
        (anomaly_df["severity"] == "critical").sum()
    )

    high_count = int(
        (anomaly_df["severity"] == "high").sum()
    )

    medium_count = int(
        (anomaly_df["severity"] == "medium").sum()
    )

    spike_count = int(
        (anomaly_df["direction"] == "spike").sum()
    )

    drop_count = int(
        (anomaly_df["direction"] == "drop").sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Anomalies",
        f"{len(anomaly_df):,}",
    )

    c2.metric(
        "Critical / High",
        f"{critical_count + high_count:,}",
    )

    c3.metric(
        "Sales Spikes",
        f"{spike_count:,}",
    )

    c4.metric(
        "Sales Drops",
        f"{drop_count:,}",
    )

    st.write("")

    # --------------------------------------------------------
    # ANOMALY TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Anomaly Revenue Pattern</div>',
        unsafe_allow_html=True,
    )

    chart_df = anomaly_df.copy()

    chart_df["Date"] = pd.to_datetime(
        chart_df["date"]
    )

    anomaly_chart = (
        alt.Chart(chart_df)
        .mark_circle(size=90)
        .encode(
            x=alt.X(
                "Date:T",
                title="Date",
            ),
            y=alt.Y(
                "revenue:Q",
                title="Revenue",
            ),
            size=alt.Size(
                "anomaly_score:Q",
                title="Anomaly Score",
            ),
            tooltip=[
                "date",
                "orders",
                "revenue",
                "anomaly_score",
                "severity",
                "direction",
            ],
        )
        .properties(height=350)
    )

    st.altair_chart(
        anomaly_chart,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Detected Events</div>',
        unsafe_allow_html=True,
    )

    f1, f2 = st.columns(2)

    with f1:
        severity_filter = st.multiselect(
            "Severity",
            ["critical", "high", "medium"],
            default=["critical", "high", "medium"],
        )

    with f2:
        direction_filter = st.multiselect(
            "Direction",
            ["spike", "drop"],
            default=["spike", "drop"],
        )

    filtered_df = anomaly_df[
        anomaly_df["severity"].isin(severity_filter)
        & anomaly_df["direction"].isin(direction_filter)
    ].copy()

    # --------------------------------------------------------
    # EXPLANATIONS
    # --------------------------------------------------------

    for _, row in filtered_df.head(10).iterrows():

        if row["severity"] == "critical":
            box = st.error
        elif row["severity"] == "high":
            box = st.warning
        else:
            box = st.info

        box(
            f"{str(row['date'])} | "
            f"{str(row['direction']).upper()} | "
            f"{str(row['severity']).upper()}\n\n"
            f"Revenue: ${row['revenue']:,.2f} | "
            f"Orders: {int(row['orders']):,} | "
            f"Anomaly Score: {row['anomaly_score']:.1f}\n\n"
            f"Revenue deviation: {row['revenue_deviation_pct']:+.2f}% | "
            f"Order deviation: {row['order_deviation_pct']:+.2f}%\n\n"
            f"{row['reason']}\n\n"
            f"Business impact: {row['business_impact']}"
        )

    # --------------------------------------------------------
    # FULL TABLE
    # --------------------------------------------------------

    display_df = filtered_df[
        [
            "date",
            "orders",
            "revenue",
            "avg_order_value",
            "anomaly_score",
            "severity",
            "direction",
            "order_deviation_pct",
            "revenue_deviation_pct",
        ]
    ].copy()

    display_df.columns = [
        "Date",
        "Orders",
        "Revenue",
        "AOV",
        "Anomaly Score",
        "Severity",
        "Direction",
        "Order Deviation %",
        "Revenue Deviation %",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )





