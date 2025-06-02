import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Set page config
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS with animation
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .animated-header {
        animation: fadeIn 2s ease-in;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Animated Header
st.markdown("""
    <div class="animated-header">
        <h1>📊 E-commerce Analytics Dashboard</h1>
        <p>Interactive Analysis of Sales Data</p>
    </div>
    """, unsafe_allow_html=True)

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload your monthly sales data (CSV)", type="csv")

# Function to load and process data
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['event_time'] = pd.to_datetime(df['event_time'])
    return df

# Load data
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    # Load default dataset if available
    default_file = Path("2019-Oct.csv")
    if default_file.exists():
        df = load_data(default_file)
    else:
        st.error("Please upload a CSV file to begin analysis")
        st.stop()

# Date filter
st.sidebar.header("Filters")
min_date = df['event_time'].min().date()
max_date = df['event_time'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data based on date range
mask = (df['event_time'].dt.date >= start_date) & (df['event_time'].dt.date <= end_date)
filtered_df = df.loc[mask]

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(filtered_df['product_id'].unique()))
with col2:
    st.metric("Highest Price", f"${filtered_df['price'].max():.2f}")
with col3:
    st.metric("Lowest Price", f"${filtered_df['price'].min():.2f}")
with col4:
    st.metric("Median Price", f"${filtered_df['price'].median():.2f}")

# Create two columns for the first row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    fig_price_dist = px.histogram(
        filtered_df,
        x="price",
        nbins=50,
        title="Product Price Distribution",
        labels={"price": "Price ($)", "count": "Number of Products"}
    )
    fig_price_dist.update_layout(showlegend=False)
    st.plotly_chart(fig_price_dist, use_container_width=True)

with col2:
    st.subheader("Top 10 Brands by Product Count")
    brand_counts = filtered_df['brand'].value_counts().head(10)
    fig_brands = px.bar(
        x=brand_counts.values,
        y=brand_counts.index,
        orientation='h',
        title="Top 10 Brands",
        labels={"x": "Number of Products", "y": "Brand"}
    )
    st.plotly_chart(fig_brands, use_container_width=True)

# Create two columns for the new brand analysis charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Brands by Total Sales Value")
    brand_sales = filtered_df.groupby('brand').agg({
        'price': lambda x: (x * filtered_df.loc[x.index, 'event_type'].eq('purchase')).sum()
    }).sort_values('price', ascending=False).head(10)
    
    fig_brand_sales = px.bar(
        brand_sales,
        x=brand_sales.index,
        y='price',
        title="Top 10 Brands by Sales Value",
        labels={"price": "Total Sales Value ($)", "brand": "Brand"},
        color='price',
        color_continuous_scale='Viridis'
    )
    fig_brand_sales.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_brand_sales, use_container_width=True)

with col2:
    st.subheader("Brands by Unique Products Sold")
    unique_products = filtered_df[filtered_df['event_type'] == 'purchase'].groupby('brand')['product_id'].nunique().sort_values(ascending=False).head(10)
    
    fig_unique_products = px.bar(
        unique_products,
        title="Top 10 Brands by Unique Products Sold",
        labels={"value": "Number of Unique Products", "brand": "Brand"},
        color='value',
        color_continuous_scale='Viridis'
    )
    fig_unique_products.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_unique_products, use_container_width=True)

# Event type distribution
st.subheader("Event Type Distribution Over Time")
events_over_time = filtered_df.groupby([filtered_df['event_time'].dt.date, 'event_type']).size().unstack()
fig_events = px.line(
    events_over_time,
    title="Event Types Over Time",
    labels={"value": "Number of Events", "index": "Date"}
)
st.plotly_chart(fig_events, use_container_width=True)

# Price ranges by category
if 'category_code' in filtered_df.columns:
    st.subheader("Price Ranges by Category")
    category_price_stats = filtered_df.groupby('category_code').agg({
        'price': ['mean', 'min', 'max']
    }).reset_index()
    category_price_stats.columns = ['category', 'mean_price', 'min_price', 'max_price']
    fig_category = px.box(
        filtered_df,
        x='category_code',
        y='price',
        title="Price Distribution by Category",
        labels={"category_code": "Category", "price": "Price ($)"}
    )
    st.plotly_chart(fig_category, use_container_width=True)

# Add data summary
st.subheader("Data Summary")
with st.expander("View Data Summary"):
    st.write("Basic Statistics of Prices:")
    st.write(filtered_df['price'].describe())
    
    if st.checkbox("Show Raw Data Sample"):
        st.write("Sample of Raw Data:")
        st.write(filtered_df.head()) 