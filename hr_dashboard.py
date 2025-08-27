"""
IBM HR Analytics Dashboard
========================
A comprehensive HR analytics dashboard replicating Tableau-style multi-sheet functionality.
Features employee demographics, attrition analysis, performance metrics, and more.

Author: AI Assistant
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# Page Configuration
st.set_page_config(
    page_title="IBM HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    /* Main styling */
    .main { padding: 20px; background-color: #f8f9fa; }
    
    /* IBM Color Palette */
    :root {
        --ibm-blue: #0f62fe;
        --ibm-gray: #525252;
        --ibm-light-blue: #4589ff;
        --ibm-green: #42be65;
        --ibm-red: #fa4d56;
        --ibm-purple: #8a3ffc;
    }
    
    /* Header styling */
    .ibm-header {
        background: linear-gradient(135deg, #0f62fe 0%, #4589ff 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid var(--ibm-blue);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Sheet navigation */
    .sheet-nav {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Filter section */
    .filter-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="ibm-header">
        <h1>🏢 IBM HR Analytics Dashboard</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">Comprehensive Employee Data Analysis & Insights</p>
    </div>
""", unsafe_allow_html=True)

# Generate Sample HR Data (if no data file is provided)
@st.cache_data
def generate_sample_hr_data():
    """Generate realistic sample HR data for demonstration"""
    np.random.seed(42)
    n_employees = 1500
    
    # Generate employee data
    departments = ['Technology', 'Sales', 'HR', 'Marketing', 'Finance', 'Operations', 'R&D']
    job_roles = ['Software Engineer', 'Data Scientist', 'Sales Rep', 'Manager', 'Analyst', 'Director', 'Specialist']
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD']
    marital_status = ['Single', 'Married', 'Divorced']
    genders = ['Male', 'Female', 'Other']
    
    data = {
        'EmployeeNumber': range(1, n_employees + 1),
        'Age': np.random.normal(35, 8, n_employees).astype(int),
        'Gender': np.random.choice(genders, n_employees, p=[0.6, 0.38, 0.02]),
        'MaritalStatus': np.random.choice(marital_status, n_employees, p=[0.4, 0.5, 0.1]),
        'Education': np.random.choice(education_levels, n_employees, p=[0.1, 0.5, 0.3, 0.1]),
        'Department': np.random.choice(departments, n_employees),
        'JobRole': np.random.choice(job_roles, n_employees),
        'YearsAtCompany': np.random.exponential(5, n_employees).astype(int),
        'MonthlyIncome': np.random.normal(7000, 2000, n_employees),
        'JobSatisfaction': np.random.randint(1, 5, n_employees),
        'PerformanceRating': np.random.choice([3, 4, 5], n_employees, p=[0.1, 0.7, 0.2]),
        'Attrition': np.random.choice(['Yes', 'No'], n_employees, p=[0.16, 0.84]),
        'DistanceFromHome': np.random.randint(1, 30, n_employees),
        'WorkLifeBalance': np.random.randint(1, 5, n_employees),
        'EnvironmentSatisfaction': np.random.randint(1, 5, n_employees),
        'YearsSinceLastPromotion': np.random.randint(0, 15, n_employees),
        'TrainingTimesLastYear': np.random.randint(0, 7, n_employees),
        'OverTime': np.random.choice(['Yes', 'No'], n_employees, p=[0.3, 0.7])
    }
    
    df = pd.DataFrame(data)
    
    # Data cleaning and adjustments
    df['Age'] = df['Age'].clip(18, 65)
    df['MonthlyIncome'] = df['MonthlyIncome'].clip(3000, 20000)
    df['YearsAtCompany'] = df['YearsAtCompany'].clip(0, 40)
    
    # Add derived columns
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100], 
                           labels=['<25', '25-35', '35-45', '45-55', '55+'])
    df['IncomeGroup'] = pd.cut(df['MonthlyIncome'], bins=[0, 5000, 7000, 10000, 100000],
                              labels=['Low', 'Medium', 'High', 'Very High'])
    df['TenureGroup'] = pd.cut(df['YearsAtCompany'], bins=[-1, 2, 5, 10, 50],
                              labels=['<2 years', '2-5 years', '5-10 years', '10+ years'])
    
    return df

# Data Upload and Loading
@st.cache_data
def load_hr_data():
    """Load HR data from file or generate sample data"""
    # Try to load from uploaded file
    uploaded_file = st.sidebar.file_uploader("Upload HR Data (CSV)", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Data loaded from uploaded file!")
        return df
    else:
        # Use sample data
        st.sidebar.info("📊 Using sample IBM HR data for demonstration")
        return generate_sample_hr_data()

# Load data
df = load_hr_data()

# Sidebar Navigation - Tableau-style Sheet Selection
st.sidebar.markdown('<div class="sheet-nav"><h3>📋 Dashboard Sheets</h3></div>', unsafe_allow_html=True)

sheet_options = {
    "🏠 Overview Dashboard": "overview",
    "👥 Employee Demographics": "demographics", 
    "📉 Attrition Analysis": "attrition",
    "⭐ Performance Metrics": "performance",
    "💰 Compensation Analysis": "compensation",
    "📊 Department Analytics": "departments",
    "📈 Trends & Insights": "trends",
    "🔍 Data Explorer": "explorer"
}

selected_sheet = st.sidebar.selectbox(
    "Select Analysis Sheet:",
    list(sheet_options.keys()),
    index=0
)
current_sheet = sheet_options[selected_sheet]

# Global Filters
st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔧 Global Filters")

# Department filter
departments = ['All'] + sorted(df['Department'].unique().tolist())
selected_departments = st.sidebar.multiselect(
    "Filter by Department:",
    departments,
    default=['All']
)

# Age group filter
age_groups = ['All'] + sorted(df['AgeGroup'].dropna().unique().tolist())
selected_age_groups = st.sidebar.multiselect(
    "Filter by Age Group:",
    age_groups,
    default=['All']
)

# Gender filter
genders = ['All'] + sorted(df['Gender'].unique().tolist())
selected_genders = st.sidebar.multiselect(
    "Filter by Gender:",
    genders,
    default=['All']
)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()

if 'All' not in selected_departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_departments)]

if 'All' not in selected_age_groups:
    filtered_df = filtered_df[filtered_df['AgeGroup'].isin(selected_age_groups)]

if 'All' not in selected_genders:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]

# Display filter summary
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Current Filters:**")
st.sidebar.write(f"Total Employees: {len(filtered_df):,}")
if len(filtered_df) > 0:
    attrition_rate = (filtered_df['Attrition'] == 'Yes').mean() * 100
    st.sidebar.write(f"Attrition Rate: {attrition_rate:.1f}%")

# Sheet Functions
def show_overview_dashboard():
    """Overview Dashboard - Key metrics and summary"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Employees", f"{len(filtered_df):,}")
    with col2:
        attrition_rate = (filtered_df['Attrition'] == 'Yes').mean() * 100
        st.metric("📉 Attrition Rate", f"{attrition_rate:.1f}%")
    with col3:
        avg_satisfaction = filtered_df['JobSatisfaction'].mean()
        st.metric("⭐ Avg Job Satisfaction", f"{avg_satisfaction:.2f}/5")
    with col4:
        avg_income = filtered_df['MonthlyIncome'].mean()
        st.metric("💰 Avg Monthly Income", f"${avg_income:,.0f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Department distribution
        dept_counts = filtered_df['Department'].value_counts()
        fig_dept = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title="Employee Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_dept.update_layout(height=400)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Attrition by department
        attrition_by_dept = filtered_df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).sort_values(ascending=True)
        
        fig_attr = px.bar(
            x=attrition_by_dept.values,
            y=attrition_by_dept.index,
            orientation='h',
            title="Attrition Rate by Department",
            labels={'x': 'Attrition Rate (%)', 'y': 'Department'},
            color=attrition_by_dept.values,
            color_continuous_scale='Reds'
        )
        fig_attr.update_layout(height=400)
        st.plotly_chart(fig_attr, use_container_width=True)

def show_demographics():
    """Employee Demographics Analysis"""
    st.markdown("## 👥 Employee Demographics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Age distribution
        fig_age = px.histogram(
            filtered_df, x='Age', 
            title="Age Distribution",
            nbins=20,
            color_discrete_sequence=['#0f62fe']
        )
        fig_age.update_layout(height=300)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Gender distribution
        gender_counts = filtered_df['Gender'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution"
        )
        fig_gender.update_layout(height=300)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col3:
        # Education levels
        edu_counts = filtered_df['Education'].value_counts()
        fig_edu = px.bar(
            x=edu_counts.index,
            y=edu_counts.values,
            title="Education Levels",
            color=edu_counts.values,
            color_continuous_scale='Blues'
        )
        fig_edu.update_layout(height=300)
        st.plotly_chart(fig_edu, use_container_width=True)
    
    # Detailed demographics table
    st.markdown("### 📊 Demographics Summary")
    demo_summary = filtered_df.groupby(['Department', 'Gender']).size().unstack(fill_value=0)
    st.dataframe(demo_summary, use_container_width=True)

def show_attrition_analysis():
    """Attrition Analysis Dashboard"""
    st.markdown("## 📉 Attrition Analysis")
    
    # Key attrition metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_attrition = (filtered_df['Attrition'] == 'Yes').sum()
    attrition_rate = (filtered_df['Attrition'] == 'Yes').mean() * 100
    avg_tenure_left = filtered_df[filtered_df['Attrition'] == 'Yes']['YearsAtCompany'].mean()
    
    with col1:
        st.metric("Total Attrition", total_attrition)
    with col2:
        st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
    with col3:
        st.metric("Avg Tenure (Left)", f"{avg_tenure_left:.1f} years")
    with col4:
        retention_rate = 100 - attrition_rate
        st.metric("Retention Rate", f"{retention_rate:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Attrition by age group
        attrition_age = filtered_df.groupby('AgeGroup')['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        fig_attr_age = px.bar(
            x=attrition_age.index,
            y=attrition_age.values,
            title="Attrition Rate by Age Group",
            labels={'y': 'Attrition Rate (%)'},
            color=attrition_age.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_attr_age, use_container_width=True)
    
    with col2:
        # Attrition by job satisfaction
        attrition_satisfaction = filtered_df.groupby('JobSatisfaction')['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        fig_attr_sat = px.line(
            x=attrition_satisfaction.index,
            y=attrition_satisfaction.values,
            title="Attrition vs Job Satisfaction",
            labels={'x': 'Job Satisfaction Level', 'y': 'Attrition Rate (%)'},
            markers=True
        )
        st.plotly_chart(fig_attr_sat, use_container_width=True)

def show_performance_metrics():
    """Performance Metrics Dashboard"""
    st.markdown("## ⭐ Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Performance rating distribution
        perf_counts = filtered_df['PerformanceRating'].value_counts().sort_index()
        fig_perf = px.bar(
            x=perf_counts.index,
            y=perf_counts.values,
            title="Performance Rating Distribution",
            labels={'x': 'Performance Rating', 'y': 'Count'},
            color=perf_counts.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        # Training vs Performance
        fig_training = px.scatter(
            filtered_df,
            x='TrainingTimesLastYear',
            y='PerformanceRating',
            title="Training vs Performance",
            trendline="ols"
        )
        st.plotly_chart(fig_training, use_container_width=True)
    
    with col3:
        # Years since promotion vs satisfaction
        fig_promo = px.scatter(
            filtered_df,
            x='YearsSinceLastPromotion',
            y='JobSatisfaction',
            title="Years Since Promotion vs Satisfaction",
            trendline="ols"
        )
        st.plotly_chart(fig_promo, use_container_width=True)

def show_compensation_analysis():
    """Compensation Analysis Dashboard"""
    st.markdown("## 💰 Compensation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary by department
        fig_salary_dept = px.box(
            filtered_df,
            x='Department',
            y='MonthlyIncome',
            title="Salary Distribution by Department"
        )
        fig_salary_dept.update_xaxes(tickangle=45)
        st.plotly_chart(fig_salary_dept, use_container_width=True)
    
    with col2:
        # Income vs Experience
        fig_income_exp = px.scatter(
            filtered_df,
            x='YearsAtCompany',
            y='MonthlyIncome',
            color='Department',
            title="Income vs Years at Company",
            trendline="ols"
        )
        st.plotly_chart(fig_income_exp, use_container_width=True)

def show_department_analytics():
    """Department-wise Analytics"""
    st.markdown("## 📊 Department Analytics")
    
    # Department metrics
    dept_metrics = filtered_df.groupby('Department').agg({
        'EmployeeNumber': 'count',
        'MonthlyIncome': 'mean',
        'JobSatisfaction': 'mean',
        'PerformanceRating': 'mean',
        'Attrition': lambda x: (x == 'Yes').mean() * 100
    }).round(2)
    
    dept_metrics.columns = ['Employee Count', 'Avg Income', 'Avg Satisfaction', 'Avg Performance', 'Attrition %']
    
    st.dataframe(dept_metrics, use_container_width=True)
    
    # Detailed department analysis
    selected_dept = st.selectbox("Select Department for Detailed Analysis:", 
                                filtered_df['Department'].unique())
    
    dept_data = filtered_df[filtered_df['Department'] == selected_dept]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_dept_age = px.histogram(
            dept_data, x='Age',
            title=f"Age Distribution - {selected_dept}",
            color_discrete_sequence=['#0f62fe']
        )
        st.plotly_chart(fig_dept_age, use_container_width=True)
    
    with col2:
        fig_dept_income = px.histogram(
            dept_data, x='MonthlyIncome',
            title=f"Income Distribution - {selected_dept}",
            color_discrete_sequence=['#42be65']
        )
        st.plotly_chart(fig_dept_income, use_container_width=True)

def show_trends_insights():
    """Trends and Insights Dashboard"""
    st.markdown("## 📈 Trends & Insights")
    
    # Correlation analysis
    numeric_cols = ['Age', 'YearsAtCompany', 'MonthlyIncome', 'JobSatisfaction', 
                   'PerformanceRating', 'DistanceFromHome', 'WorkLifeBalance']
    
    correlation_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title="Correlation Matrix - Key HR Metrics",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Key insights
    st.markdown("### 💡 Key Insights")
    
    insights = [
        f"• Highest attrition rate: {filtered_df.groupby('Department')['Attrition'].apply(lambda x: (x == 'Yes').mean()).max():.1%} in {filtered_df.groupby('Department')['Attrition'].apply(lambda x: (x == 'Yes').mean()).idxmax()}",
        f"• Average tenure: {filtered_df['YearsAtCompany'].mean():.1f} years",
        f"• Top performing department: {filtered_df.groupby('Department')['PerformanceRating'].mean().idxmax()}",
        f"• Most satisfied employees in: {filtered_df.groupby('Department')['JobSatisfaction'].mean().idxmax()}"
    ]
    
    for insight in insights:
        st.markdown(insight)

def show_data_explorer():
    """Data Explorer - Raw data view"""
    st.markdown("## 🔍 Data Explorer")
    
    st.markdown("### Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Total Columns", len(filtered_df.columns))
    with col3:
        st.metric("Missing Values", filtered_df.isnull().sum().sum())
    
    # Data preview
    st.markdown("### Data Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Column statistics
    if st.checkbox("Show Column Statistics"):
        st.markdown("### Column Statistics")
        st.dataframe(filtered_df.describe(), use_container_width=True)

# Main Dashboard Navigation
if current_sheet == "overview":
    show_overview_dashboard()
elif current_sheet == "demographics":
    show_demographics()
elif current_sheet == "attrition":
    show_attrition_analysis()
elif current_sheet == "performance":
    show_performance_metrics()
elif current_sheet == "compensation":
    show_compensation_analysis()
elif current_sheet == "departments":
    show_department_analytics()
elif current_sheet == "trends":
    show_trends_insights()
elif current_sheet == "explorer":
    show_data_explorer()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🏢 IBM HR Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>Interactive multi-sheet dashboard for comprehensive HR data analysis</p>
    </div>
""", unsafe_allow_html=True)