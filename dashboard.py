import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cafe Analytics Dashboard",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0F172A;
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload Cafe Sales Dataset",
    type=["csv"]
)

if uploaded_file is None:
    st.title("☕ Cafe Analytics Dashboard")

    st.info(
        "Upload a CSV file containing Date, Item, Quantity and Price columns."
    )

    st.stop()

df = pd.read_csv(uploaded_file)

required_columns = [
    "Date",
    "Item",
    "Quantity",
    "Price"
]

if not all(col in df.columns for col in required_columns):
    st.error(
        "Dataset must contain Date, Item, Quantity and Price columns."
    )
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = df["Quantity"] * df["Price"]

st.sidebar.title("☕ Cafe Analytics")
st.sidebar.markdown("---")

products = df["Item"].unique()

selected_product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + list(products)
)

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered_df = df.copy()

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Item"] == selected_product
    ]

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(start_date))
    &
    (filtered_df["Date"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

csv = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Quantity"].sum()

best_selling_item = (
    filtered_df.groupby("Item")["Quantity"]
    .sum()
    .idxmax()
)

highest_revenue_product = (
    filtered_df.groupby("Item")["Revenue"]
    .sum()
    .idxmax()
)

average_revenue = (
    filtered_df["Revenue"]
    .mean()
)

st.title("☕ Cafe Analytics Dashboard")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "📦 Orders",
        total_orders
    )

with col3:
    st.metric(
        "🏆 Best Seller",
        best_selling_item
    )

with col4:
    st.metric(
        "📈 Top Revenue Product",
        highest_revenue_product
    )

with col5:
    st.metric(
        "💵 Avg Revenue",
        f"₹{average_revenue:,.0f}"
    )

daily_revenue = (
    filtered_df.groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

revenue_trend_chart = px.line(
    daily_revenue,
    x="Date",
    y="Revenue",
    title="Daily Revenue Trend",
    markers=True
)

revenue_trend_chart.update_layout(
    template="plotly_dark"
)

items_quantity = (
    filtered_df.groupby("Item")["Quantity"]
    .sum()
    .reset_index()
)

quantity_chart = px.bar(
    items_quantity,
    x="Item",
    y="Quantity",
    color="Item",
    title="Quantity Sold by Product"
)

quantity_chart.update_layout(
    template="plotly_dark"
)

items_by_revenue = (
    filtered_df.groupby("Item")["Revenue"]
    .sum()
    .reset_index()
)

revenue_chart = px.bar(
    items_by_revenue,
    x="Item",
    y="Revenue",
    color="Item",
    title="Revenue by Product"
)

revenue_chart.update_layout(
    template="plotly_dark"
)

revenue_share_chart = px.pie(
    items_by_revenue,
    names="Item",
    values="Revenue",
    title="Revenue Share by Product"
)

revenue_share_chart.update_layout(
    template="plotly_dark"
)

monthly_revenue = (
    filtered_df.groupby(
        filtered_df["Date"].dt.to_period("M")
    )["Revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["Date"] = (
    monthly_revenue["Date"]
    .astype(str)
)

monthly_chart = px.line(
    monthly_revenue,
    x="Date",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True
)

monthly_chart.update_layout(
    template="plotly_dark"
)

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "💰 Revenue",
        "📦 Products"
    ]
)

with tab1:
    st.plotly_chart(
        revenue_trend_chart,
        use_container_width=True
    )

with tab2:
    st.plotly_chart(
        monthly_chart,
        use_container_width=True
    )

with tab3:

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            quantity_chart,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            revenue_chart,
            use_container_width=True
        )

    st.plotly_chart(
        revenue_share_chart,
        use_container_width=True
    )

with st.expander("📄 View Dataset"):
    st.dataframe(filtered_df)

st.markdown("---")

st.caption(
    "Built with Python, Pandas, Plotly and Streamlit"
)