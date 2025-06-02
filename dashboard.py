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
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
# -------------
st.markdown("""
    <style>
    /* Main page styling */
    .main {
        padding: 20px;
        background-color: #f8f9fa;
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .stMetric:hover {
        transform: translateY(-2px);
    }
    
    /* Header animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Animated header */
    .animated-header {
        animation: fadeIn 1.5s ease-out;
        padding: 30px;
        border-radius: 15px;
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Section styling */
    .section-header {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 10px 15px;
        border-radius: 8px;
        margin: 20px 0;
        color: #1a1a1a;
        font-weight: 600;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #6dd5ed;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    
    /* Custom text styles */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #2193b0;
    }
    p {
        font-family: 'Helvetica Neue', sans-serif;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
# -------------
st.markdown("""
    <div class="animated-header">
        <h1>📊 E-commerce Analytics Dashboard</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">Interactive Analysis of Sales Data</p>
    </div>
    """, unsafe_allow_html=True)

# File Upload Section
# -----------------
st.markdown('<div class="section-header">Data Input</div>', unsafe_allow_html=True)
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
st.sidebar.markdown('<div class="section-header">Analysis Controls</div>', unsafe_allow_html=True)
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
st.markdown('<div class="section-header">Key Performance Metrics</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

metric_style = """
    <style>
    .metric-value { font-size: 24px; font-weight: bold; color: #2193b0; }
    .metric-label { font-size: 14px; color: #666; }
    </style>
"""
st.markdown(metric_style, unsafe_allow_html=True)

with col1:
    st.metric("Total Products", len(filtered_df['product_id'].unique()))
with col2:
    st.metric("Highest Price", f"${filtered_df['price'].max():.2f}")
with col3:
    st.metric("Lowest Price", f"${filtered_df['price'].min():.2f}")
with col4:
    st.metric("Median Price", f"${filtered_df['price'].median():.2f}")

# Chart Theme Configuration
chart_theme = {
    'bgcolor': 'white',
    'font_family': 'Helvetica Neue',
    'title_font_size': 20,
    'title_font_color': '#2193b0',
    'showgrid': True,
    'gridcolor': '#f0f0f0'
}

# Price Distribution Analysis
# -------------------------
st.markdown('<div class="section-header">Price Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_price_dist = px.histogram(
        filtered_df,
        x="price",
        nbins=50,
        title="Product Price Distribution",
        labels={"price": "Price ($)", "count": "Number of Products"},
        color_discrete_sequence=['#2193b0']
    )
    fig_price_dist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family=chart_theme['font_family'],
        title_font_size=chart_theme['title_font_size'],
        title_font_color=chart_theme['title_font_color']
    )
    st.plotly_chart(fig_price_dist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    brand_counts = filtered_df['brand'].value_counts().head(10)
    fig_brands = px.bar(
        x=brand_counts.values,
        y=brand_counts.index,
        orientation='h',
        title="Top 10 Brands",
        labels={"x": "Number of Products", "y": "Brand"},
        color=brand_counts.values,
        color_continuous_scale='Viridis'
    )
    fig_brands.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family=chart_theme['font_family'],
        title_font_size=chart_theme['title_font_size'],
        title_font_color=chart_theme['title_font_color']
    )
    st.plotly_chart(fig_brands, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced Brand Analysis
# ---------------------
st.markdown('<div class="section-header">Brand Performance Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
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
    fig_brand_sales.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family=chart_theme['font_family'],
        title_font_size=chart_theme['title_font_size'],
        title_font_color=chart_theme['title_font_color']
    )
    st.plotly_chart(fig_brand_sales, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    unique_products = filtered_df[filtered_df['event_type'] == 'purchase'].groupby('brand')['product_id'].nunique().sort_values(ascending=False).head(10)
    
    fig_unique_products = px.bar(
        unique_products,
        title="Top 10 Brands by Unique Products Sold",
        labels={"value": "Number of Unique Products", "brand": "Brand"},
        color='value',
        color_continuous_scale='Viridis'
    )
    fig_unique_products.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family=chart_theme['font_family'],
        title_font_size=chart_theme['title_font_size'],
        title_font_color=chart_theme['title_font_color']
    )
    st.plotly_chart(fig_unique_products, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Time Series Analysis
# ------------------
st.markdown('<div class="section-header">Temporal Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
events_over_time = filtered_df.groupby([filtered_df['event_time'].dt.date, 'event_type']).size().unstack()
fig_events = px.line(
    events_over_time,
    title="Event Types Over Time",
    labels={"value": "Number of Events", "index": "Date"},
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_events.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family=chart_theme['font_family'],
    title_font_size=chart_theme['title_font_size'],
    title_font_color=chart_theme['title_font_color']
)
st.plotly_chart(fig_events, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Category Analysis
# ---------------
if 'category_code' in filtered_df.columns:
    st.markdown('<div class="section-header">Category Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_category = px.box(
        filtered_df,
        x='category_code',
        y='price',
        title="Price Distribution by Category",
        labels={"category_code": "Category", "price": "Price ($)"},
        color='category_code',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_category.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family=chart_theme['font_family'],
        title_font_size=chart_theme['title_font_size'],
        title_font_color=chart_theme['title_font_color']
    )
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Data Summary Section
# ------------------
st.markdown('<div class="section-header">Detailed Analysis</div>', unsafe_allow_html=True)
with st.expander("View Data Summary"):
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.write("### Basic Statistics of Prices")
    st.write(filtered_df['price'].describe())
    
    if st.checkbox("Show Raw Data Sample"):
        st.write("### Sample of Raw Data")
        st.write(filtered_df.head())
    st.markdown('</div>', unsafe_allow_html=True) 