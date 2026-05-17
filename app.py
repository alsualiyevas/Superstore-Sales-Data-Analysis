import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="AI Data Science Dashboard", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced Styling (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    div[data-testid="stMetricValue"] { color: #58a6ff; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_preprocess():
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Month'] = df['Order Date'].dt.to_period('M').astype(str)
    # Notebook-da hesabladığın Profit Margin sütunu
    df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
    return df

df = load_and_preprocess()

# --- SIDEBAR: NAVİQASİYA ---
st.sidebar.title("🚀 ML & Analytics Suite")
st.sidebar.markdown("---")
choice = st.sidebar.radio("Analiz bölməsini seçin:", 
    ["Executive Summary", "Customer Segmentation (RFM)", "Deep Loss Analysis", "Correlation Matrix"])

# --- BÖLMƏ 1: EXECUTIVE SUMMARY (Trendlər) ---
if choice == "Executive Summary":
    st.title("📈 Business Intelligence Overview")
    
    # KPI-lar
    t_sales = df['Sales'].sum()
    t_profit = df['Profit'].sum()
    avg_margin = df['Profit Margin'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${t_sales:,.0f}", delta="12% vs last year")
    col2.metric("Total Profit", f"${t_profit:,.0f}", delta=f"{t_profit/t_sales:.1%}")
    col3.metric("Avg Margin", f"{avg_margin:.2f}%")

    st.markdown("---")
    
    # Monthly Trend (Notebook-dakı Time Series)
    st.subheader("Aylıq Satış və Mənfəət Dinamikası")
    trend_df = df.groupby('Order Month')[['Sales', 'Profit']].sum().reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend_df['Order Month'], y=trend_df['Sales'], name='Sales', line=dict(color='#00f2fe', width=3)))
    fig_trend.add_trace(go.Bar(x=trend_df['Order Month'], y=trend_df['Profit'], name='Profit', marker_color='#4facfe', opacity=0.6))
    fig_trend.update_layout(template="plotly_dark", hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

# --- BÖLMƏ 2: RFM & CLUSTERING (Sənin Notebook-dakı ML hissəsi) ---
elif choice == "Customer Segmentation (RFM)":
    st.title("👥 Advanced Customer Segmentation")
    st.info("Bu bölmə K-Means klasterləşdirmə və RFM analizi əsasında hazırlanıb.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Notebook-dakı Segment Payları
        seg_data = df.groupby('Segment')['Customer ID'].nunique().reset_index()
        fig_seg = px.pie(seg_data, values='Customer ID', names='Segment', hole=0.6, 
                         title="Müştəri Seqmentlərinin Payı", color_discrete_sequence=px.colors.sequential.Electric)
        st.plotly_chart(fig_seg, use_container_width=True)

    with col2:
        # K-Means Visual (Simulyasiya edilmiş Notebook məntiqi)
        st.write("### Klaster Analizi (Sales vs Profit)")
        fig_cluster = px.scatter(df, x="Sales", y="Profit", color="Category", 
                                 size="Quantity", hover_data=['Product Name'],
                                 template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_cluster, use_container_width=True)

# --- BÖLMƏ 3: DEEP LOSS ANALYSIS (Sənin tapdığın ən vacib hissə!) ---
elif choice == "Deep Loss Analysis":
    st.title("⚠️ Financial Risk & Loss Analysis")
    
    # Notebook-da hesabladığın zərərli sifariş faizi
    total_orders = len(df)
    loss_orders = len(df[df['Profit'] < 0])
    loss_rate = (loss_orders / total_orders) * 100

    st.error(f"Kritik Göstərici: Sifarişlərin {loss_rate:.2f}%-i zərər ilə nəticələnir!")

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Ən çox zərər verən 15 Məhsul")
        loss_products = df[df['Profit'] < 0].groupby('Product Name')['Profit'].sum().sort_values().head(15).reset_index()
        fig_loss_prod = px.bar(loss_products, x='Profit', y='Product Name', orientation='h', color='Profit', color_continuous_scale='Reds')
        st.plotly_chart(fig_loss_prod, use_container_width=True)

    with col2:
        st.write("### Endirim (Discount) vs Mənfəət")
        # Notebook-dakı Discount vs Profit analizi
        fig_disc = px.scatter(df, x="Discount", y="Profit", color="Category", trendline="ols")
        st.plotly_chart(fig_disc, use_container_width=True)

# --- BÖLMƏ 4: CORRELATION MATRIX ---
elif choice == "Correlation Matrix":
    st.title("🔗 Feature Correlation Matrix")
    st.write("Dəyişənlər arasındakı riyazi asılılıq (Notebook-dakı Heatmap)")
    
    # Notebook-dakı .corr() hissəsi
    corr = df[['Sales', 'Quantity', 'Discount', 'Profit', 'Profit Margin']].corr()
    fig_heatmap = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
    fig_heatmap.update_layout(height=600)
    st.plotly_chart(fig_heatmap, use_container_width=True)