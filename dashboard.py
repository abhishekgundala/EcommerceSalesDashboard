"""
E-commerce Analytics Dashboard
----------------------------
A comprehensive analytics dashboard for visualizing e-commerce data.
Built with Streamlit and Plotly for interactive data exploration.

Author: Abhishek Gundala
Version: 1.0.0
License: MIT
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Configuration and Setup
# ----------------------
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
# -------------
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

# Header Section
# -------------
st.markdown("""
    <div class="animated-header">
        <h1>📊 E-commerce Analytics Dashboard</h1>
        <p>Interactive Analysis of Sales Data</p>
    </div>
    """, unsafe_allow_html=True)

# File Upload Section
# -----------------
uploaded_file = st.file_uploader("Upload your monthly sales data (CSV)", type="csv")

@st.cache_data
def load_data(file_path):
    """
    Load and preprocess the e-commerce data from CSV.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV file containing e-commerce data
        
    Returns:
    --------
    pd.DataFrame
        Processed DataFrame with converted timestamps
    """
    df = pd.read_csv(file_path)
    df['event_time'] = pd.to_datetime(df['event_time'])
    return df

# Data Loading
# -----------
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    default_file = Path("2019-Oct.csv")
    if default_file.exists():
        df = load_data(default_file)
    else:
        st.error("Please upload a CSV file to begin analysis")
        st.stop()

# Sidebar Filters
# --------------
st.sidebar.header("Filters")
min_date = df['event_time'].min().date()
max_date = df['event_time'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Data Filtering
# -------------
mask = (df['event_time'].dt.date >= start_date) & (df['event_time'].dt.date <= end_date)
filtered_df = df.loc[mask]

# Key Metrics Section
# -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(filtered_df['product_id'].unique()))
with col2:
    st.metric("Highest Price", f"${filtered_df['price'].max():.2f}")
with col3:
    st.metric("Lowest Price", f"${filtered_df['price'].min():.2f}")
with col4:
    st.metric("Median Price", f"${filtered_df['price'].median():.2f}")

# Price Distribution Analysis
# -------------------------
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

# Brand Analysis
# -------------
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

# Advanced Brand Analysis
# ---------------------
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

# Time Series Analysis
# ------------------
st.subheader("Event Type Distribution Over Time")
events_over_time = filtered_df.groupby([filtered_df['event_time'].dt.date, 'event_type']).size().unstack()
fig_events = px.line(
    events_over_time,
    title="Event Types Over Time",
    labels={"value": "Number of Events", "index": "Date"}
)
st.plotly_chart(fig_events, use_container_width=True)

# Category Analysis
# ---------------
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

# Data Summary Section
# ------------------
st.subheader("Data Summary")
with st.expander("View Data Summary"):
    st.write("Basic Statistics of Prices:")
    st.write(filtered_df['price'].describe())
    
    if st.checkbox("Show Raw Data Sample"):
        st.write("Sample of Raw Data:")
        st.write(filtered_df.head()) 