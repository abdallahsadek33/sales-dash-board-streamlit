
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #F5F5F5;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .stMetric label {color: #004B87 !important; font-weight: bold !important; font-size: 14px !important;}
    .stMetric [data-testid="stMetricValue"] {color: #00A3E0 !important; font-size: 28px !important; font-weight: bold !important;}
    h1, h2, h3 {color: #004B87 !important;}
    </style>
    """, unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    fact_sales = pd.read_csv('FactSale.csv')
    dim_customer = pd.read_csv('DimCustomer.csv', encoding='latin-1')
    dim_city = pd.read_csv('DimCity.csv', encoding='latin-1')
    dim_stock = pd.read_csv('DimStockItem.csv', encoding='latin-1')
    dim_employee = pd.read_excel('DimEmployee.xlsx')

    fact_sales['Invoice Date Key'] = pd.to_datetime(fact_sales['Invoice Date Key'])
    fact_sales['Year'] = fact_sales['Invoice Date Key'].dt.year
    fact_sales['Quarter'] = 'Q' + fact_sales['Invoice Date Key'].dt.quarter.astype(str)
    fact_sales['Year-Month'] = fact_sales['Invoice Date Key'].dt.to_period('M').astype(str)

    dim_customer_clean = dim_customer.iloc[1:].copy()
    dim_customer_clean.columns = dim_customer.iloc[0]
    dim_customer_clean['Customer Key'] = pd.to_numeric(dim_customer_clean['Customer Key'], errors='coerce')

    dim_stock_clean = dim_stock.iloc[1:].copy()
    dim_stock_clean.columns = dim_stock.iloc[0]
    dim_stock_clean['Stock Item Key'] = pd.to_numeric(dim_stock_clean['Stock Item Key'], errors='coerce')

    fact_enriched = fact_sales.merge(dim_customer_clean[['Customer Key', 'Customer']], on='Customer Key', how='left')
    fact_enriched = fact_enriched.merge(dim_city[['City Key', 'City', 'State Province', 'Sales Territory']], on='City Key', how='left')
    fact_enriched = fact_enriched.merge(dim_stock_clean[['Stock Item Key', 'Stock Item']], on='Stock Item Key', how='left')
    fact_enriched = fact_enriched.merge(dim_employee[['Employee Key', 'Preferred Name']], left_on='Salesperson Key', right_on='Employee Key', how='left')

    return fact_enriched

df = load_data()

# Sidebar
st.sidebar.title("🔍 Filters")
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)
quarters = sorted(df['Quarter'].unique())
selected_quarters = st.sidebar.multiselect("Quarter", quarters, default=quarters)
territories = df['Sales Territory'].dropna().unique()
selected_territories = st.sidebar.multiselect("Territory", territories, default=territories)

df_filtered = df[(df['Year'].isin(selected_years)) & (df['Quarter'].isin(selected_quarters)) & (df['Sales Territory'].isin(selected_territories))]

# Header
st.title("📊 Sales Performance Dashboard")
st.subheader("Tailspin Toys - Executive Overview")
st.markdown("---")

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💰 Revenue", f"${df_filtered['Total Including Tax'].sum():,.0f}")
with col2:
    st.metric("📈 Profit", f"${df_filtered['Profit'].sum():,.0f}")
with col3:
    margin = (df_filtered['Profit'].sum() / df_filtered['Total Excluding Tax'].sum() * 100)
    st.metric("📊 Margin", f"{margin:.1f}%")
with col4:
    st.metric("🛒 Orders", f"{df_filtered['WWI Invoice ID'].nunique():,}")
with col5:
    avg = df_filtered['Total Including Tax'].sum() / df_filtered['WWI Invoice ID'].nunique()
    st.metric("💵 Avg Order", f"${avg:,.0f}")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trend")
    monthly = df_filtered.groupby('Year-Month')['Total Including Tax'].sum().reset_index()
    fig = px.line(monthly, x='Year-Month', y='Total Including Tax')
    fig.update_traces(line_color='#00A3E0', line_width=3)
    fig.update_layout(
        height=350,
        xaxis_title="Period",
        yaxis_title="Revenue ($)",
        plot_bgcolor='white',
        font=dict(color='#2C3E50', size=11)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💹 Profit Trend")
    monthly_p = df_filtered.groupby('Year-Month').agg({'Profit': 'sum', 'Total Excluding Tax': 'sum'}).reset_index()
    monthly_p['Margin'] = (monthly_p['Profit'] / monthly_p['Total Excluding Tax'] * 100)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly_p['Year-Month'], y=monthly_p['Profit'], name='Profit', marker_color='#28A745'), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly_p['Year-Month'], y=monthly_p['Margin'], name='Margin %', line=dict(color='#FFA500', width=3)), secondary_y=True)
    fig.update_layout(height=350, plot_bgcolor='white', font=dict(color='#2C3E50', size=11))
    fig.update_yaxes(title_text="Profit ($)", secondary_y=False)
    fig.update_yaxes(title_text="Margin (%)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products")
    top_prod = df_filtered.groupby('Description')['Total Including Tax'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_prod, y='Description', x='Total Including Tax', orientation='h', color='Total Including Tax', color_continuous_scale='Blues')
    fig.update_layout(
        height=400,
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Revenue ($)",
        yaxis_title="",
        plot_bgcolor='white',
        font=dict(color='#2C3E50', size=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌍 Sales by Territory")
    terr = df_filtered.groupby('Sales Territory')['Total Including Tax'].sum().reset_index()
    fig = px.pie(terr, values='Total Including Tax', names='Sales Territory', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white', size=14))
    fig.update_layout(height=400, font=dict(color='#2C3E50', size=11))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 3
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Top 10 Customers")
    top_cust = df_filtered[df_filtered['Customer Key'] != 0].groupby('Customer')['Total Including Tax'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_cust, y='Customer', x='Total Including Tax', orientation='h', color='Total Including Tax', color_continuous_scale='Greens')
    fig.update_layout(
        height=400,
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Revenue ($)",
        yaxis_title="",
        plot_bgcolor='white',
        font=dict(color='#2C3E50', size=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Top 10 Salespeople")
    top_sales = df_filtered[df_filtered['Preferred Name'].notna()].groupby('Preferred Name')['Total Including Tax'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_sales, x='Preferred Name', y='Total Including Tax', color='Total Including Tax', color_continuous_scale='Oranges')
    fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="Revenue ($)",
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        font=dict(color='#2C3E50', size=10)
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Geographic
st.subheader("🗺️ Sales by State")
states = df_filtered.groupby('State Province').agg({'Total Including Tax': 'sum', 'Profit': 'sum'}).reset_index()
states['Margin'] = (states['Profit'] / (states['Total Including Tax'] - states['Profit']) * 100)
states = states.sort_values('Total Including Tax', ascending=False).head(15)

fig = px.bar(states, x='State Province', y='Total Including Tax', color='Margin', color_continuous_scale='RdYlGn')
fig.update_layout(
    height=400,
    xaxis_tickangle=-45,
    xaxis_title="State",
    yaxis_title="Revenue ($)",
    plot_bgcolor='white',
    font=dict(color='#2C3E50', size=10)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Data Table
st.subheader("📋 Detailed Data")
with st.expander("View Transactions"):
    cols = ['Invoice Date Key', 'Customer', 'Description', 'Quantity', 'Unit Price', 'Total Including Tax', 'Profit', 'State Province']
    st.dataframe(df_filtered[cols].head(100), use_container_width=True, height=400)

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center; color:#004B87; padding:20px;'><b>Tailspin Toys Sales Dashboard</b><br>2013-2016 | Streamlit & Plotly</div>", unsafe_allow_html=True)
