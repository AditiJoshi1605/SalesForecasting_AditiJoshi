import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import calendar
import os

# ───────────────────────── Page Configuration ─────────────────────────
st.set_page_config(
    page_title="Superstore Sales Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────── Custom CSS ─────────────────────────
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Metric cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
    border: 1px solid #3a3a5c;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
div[data-testid="stMetric"] label {
    color: #a0a0c0 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #e0e0ff !important;
    font-weight: 700 !important;
}

/* ── Insight card ── */
.insight-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #22223a 100%);
    border-left: 4px solid #6c63ff;
    border-radius: 10px;
    padding: 18px 22px;
    margin: 10px 0;
    color: #c8c8e0;
    font-size: 0.92rem;
    line-height: 1.7;
}
.insight-card strong {
    color: #a29bfe;
}

/* ── Section header ── */
.section-header {
    background: linear-gradient(135deg, #6c63ff 0%, #a29bfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 1.6rem;
    margin: 30px 0 12px 0;
}

/* ── Recommendation pill ── */
.rec-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #22223a 100%);
    border: 1px solid #3a3a5c;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #c8c8e0;
    font-size: 0.92rem;
    line-height: 1.65;
}

/* ── Chart container ── */
.chart-container img {
    border-radius: 10px;
    border: 1px solid #2a2a40;
}

/* ── Expander tweaks ── */
details[data-testid="stExpander"] {
    border: 1px solid #3a3a5c !important;
    border-radius: 10px !important;
    background: #1a1a2e !important;
}

/* ── Divider ── */
hr {
    border-color: #2a2a40 !important;
}

/* ── DataFrame ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# ───────────────────────── Load Dataset ─────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed", dayfirst=True)
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()
    df["Quarter"] = df["Order Date"].dt.quarter
    return df

df = load_data()


# ───────────────────────── Helpers ─────────────────────────
def insight_html(text: str) -> None:
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)

def section_title(text: str) -> None:
    st.markdown(f'<p class="section-header">{text}</p>', unsafe_allow_html=True)

def format_sales(val) -> str:
    return f"${val:,.2f}"


# ═══════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════
st.sidebar.info("📦 End-to-End Sales Forecasting & Demand Intelligence System")
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "1. Sales Overview",
        "2. Forecast Explorer",
        "3. Anomaly Report",
        "4. Product Demand Segments"
    ]
)

# ═══════════════════════════════════════════════════════════════════════
#  PAGE 1: SALES OVERVIEW
# ═══════════════════════════════════════════════════════════════════════
if page == "1. Sales Overview":
    st.markdown("## 📊 Sales Overview Dashboard")
    st.caption("Analyzing historical sales patterns and filtering dataset performance.")
    st.divider()

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        selected_category = st.selectbox("Filter by Category", ["All"] + list(df['Category'].unique()))
    with col_f2:
        selected_region = st.selectbox("Filter by Region", ["All"] + list(df['Region'].unique()))
    with col_f3:
        selected_year = st.selectbox("Filter by Year", ["All"] + sorted(list(df['Year'].unique())))
        
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]

    with st.expander("🗃️ Dataset Preview", expanded=False):
        st.dataframe(filtered_df.head(10), width='stretch')

    section_title("📋 Business KPIs")

    total_sales = filtered_df["Sales"].sum()
    avg_sales = filtered_df["Sales"].mean()
    total_orders = filtered_df["Order ID"].nunique()
    avg_shipping = filtered_df["Shipping Days"].mean()
    top_cat = filtered_df.groupby("Category")["Sales"].sum().idxmax() if not filtered_df.empty else "N/A"

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Records", f"{filtered_df.shape[0]:,}")
    m2.metric("Total Sales", f"${total_sales/1000000:.2f} M" if total_sales >= 1000000 else format_sales(total_sales))
    m3.metric("Avg Order Value", format_sales(avg_sales) if pd.notnull(avg_sales) else "$0")
    m4.metric("Unique Orders", f"{total_orders:,}")
    m5.metric("Avg Ship Days", f"{avg_shipping:.1f}" if pd.notnull(avg_shipping) else "0")
    m6.metric("Highest Revenue Category", top_cat)

    st.divider()
    section_title("📈 Sales Trends")
    
    col_bar, col_line = st.columns(2)
    with col_bar:
        st.markdown("#### Sales by Year")
        if os.path.exists("charts/yearly_sales.png"):
            st.image("charts/yearly_sales.png", width='stretch')
            
    with col_line:
        st.markdown("#### Monthly Sales Trend")
        if os.path.exists("charts/monthly_sales.png"):
            st.image("charts/monthly_sales.png", width='stretch')
            
    st.markdown("#### 💡 Business Insights")
    insight_html(
        "<ul>"
        "<li>Highest sales occurred in <strong>Nov 2018</strong>.</li>"
        "<li>Lowest sales occurred in <strong>Feb 2015</strong>.</li>"
        "<li>Overall sales show an <strong>increasing trend</strong> over four years.</li>"
        "<li><strong>Technology</strong> contributed the highest revenue.</li>"
        "<li><strong>West</strong> region generated the strongest sales performance.</li>"
        "</ul>"
    )


# ═══════════════════════════════════════════════════════════════════════
#  PAGE 2: FORECAST EXPLORER
# ═══════════════════════════════════════════════════════════════════════
elif page == "2. Forecast Explorer":
    st.markdown("## 🔮 Forecast Explorer")
    st.caption("Compare forecasting models and explore category/region level predictions.")
    st.divider()

    # Model Selection
    model_choice = st.selectbox("Select Forecasting Model Output to View", ["XGBoost", "SARIMA", "Prophet"])
    
    col_chart, col_space = st.columns([2, 1])
    with col_chart:
        if model_choice == "XGBoost" and os.path.exists("charts/xgboost_forecast.png"):
            st.image("charts/xgboost_forecast.png", width='stretch')
        elif model_choice == "SARIMA" and os.path.exists("charts/sarima_forecast.png"):
            st.image("charts/sarima_forecast.png", width='stretch')
        elif model_choice == "Prophet" and os.path.exists("charts/prophet_forecast.png"):
            st.image("charts/prophet_forecast.png", width='stretch')

    with col_space:
        if os.path.exists('model_comparison.csv'):
            st.markdown("**Model Performance Metrics**")
            comp_df = pd.read_csv('model_comparison.csv')
            display_df = comp_df[['Model', 'MAE', 'RMSE', 'MAPE']].copy()
            display_df['MAE'] = display_df['MAE'].apply(lambda x: f"${x:,.0f}")
            display_df['RMSE'] = display_df['RMSE'].apply(lambda x: f"${x:,.0f}")
            display_df['MAPE'] = display_df['MAPE'].apply(lambda x: f"{x*100:.1f}%")
            st.dataframe(display_df, hide_index=True)
            
            best_model = comp_df.loc[comp_df['RMSE'].idxmin(), 'Model']
            insight_html(f"<strong>🏆 Best Model:</strong> {best_model}<br>Lowest RMSE & MAPE — predictions are closest to actual sales.")

    st.divider()
    section_title("📌 Category & Region Forecasts")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        if os.path.exists('charts/category_region_forecast.png'):
            st.image('charts/category_region_forecast.png', width='stretch')
            
    with c2:
        st.markdown("**Forecast Horizon Viewer**")
        horizon = st.slider("Months Ahead", min_value=1, max_value=3, value=1)
        
        if os.path.exists('task4_forecasts.csv'):
            f_df = pd.read_csv('task4_forecasts.csv', index_col=0)
            col_name = f"Month {horizon} Forecast"
            st.dataframe(f_df[[col_name]].style.format({col_name: "${:,.2f}"}))
            
            best_seg = f_df['Total Expected Growth'].idxmax()
            insight_html(f"<strong>🚀 Strongest Growth Segment:</strong> {best_seg}<br>Ensure inventory buffers are in place to meet this predicted demand.")


# ═══════════════════════════════════════════════════════════════════════
#  PAGE 3: ANOMALY REPORT
# ═══════════════════════════════════════════════════════════════════════
elif page == "3. Anomaly Report":
    st.markdown("## 🚨 Anomaly Report")
    st.caption("Identifying unusual sales spikes or drops using Isolation Forest and Z-Score detection.")
    st.divider()

    if os.path.exists('anomalies.csv'):
        adf = pd.read_csv('anomalies.csv')
        total_weeks = 209
        anomalies_found = len(adf)
        spikes = len(adf[adf['Type'] == 'Spike'])
        drops = len(adf[adf['Type'] == 'Drop'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Weeks Analyzed", total_weeks)
        m2.metric("Anomalies Found", anomalies_found)
        m3.metric("Positive Spikes", spikes)
        m4.metric("Negative Drops", drops)
        st.divider()

        c_top, c_meth = st.columns([2, 1])
        with c_top:
            st.markdown("#### Top 5 Highest Anomalies")
            top5 = adf.sort_values(by='Sales', ascending=False).head(5)
            top5['Date_fmt'] = pd.to_datetime(top5['Date']).dt.strftime('%Y-%m')
            
            t_cols = st.columns(5)
            for i, (_, row) in enumerate(top5.iterrows()):
                t_cols[i].metric(row['Date_fmt'], format_sales(row['Sales']))
                
        with c_meth:
            st.markdown("#### Detection Methods")
            insight_html("✔ Isolation Forest<br>✔ Z-Score Detection<br><br><strong>Confidence:</strong> High")

        st.divider()
        st.markdown("#### Anomaly Log")
        table_df = adf[['Date', 'Sales', 'Type', 'Possible Reason']].copy()
        table_df['Date'] = pd.to_datetime(table_df['Date']).dt.strftime('%Y-%m-%d')
        table_df['Sales'] = table_df['Sales'].apply(format_sales)
        
        c_table, c_comp = st.columns([2, 1])
        with c_table:
            st.dataframe(table_df, width='stretch', hide_index=True)
            
        with c_comp:
            st.markdown("#### Method Comparison")
            insight_html(
                "<strong>Isolation Forest:</strong> 11 anomalies<br>"
                "<strong>Z-score:</strong> 11 anomalies<br>"
                "<strong>Common:</strong> 5 anomalies"
            )
            
    st.divider()
    
    st.markdown("#### Superstore Sales Anomalies")
    if os.path.exists("charts/anomaly_detection.png"):
        st.image("charts/anomaly_detection.png", width='stretch')
        
    st.divider()
    st.markdown("#### Supplementary Dataset Validation")
    st.markdown("The same anomaly detection pipeline was validated on the Video Game Sales dataset, demonstrating that the approach generalizes across domains.")
    if os.path.exists("charts/video_game_anomaly.png"):
        st.image("charts/video_game_anomaly.png", width='stretch')

    st.markdown("#### 💡 Business Interpretation")
    insight_html(
        "<ul>"
        "<li>Holiday sales create positive spikes.</li>"
        "<li>Promotions increase demand.</li>"
        "<li>Supply shortages create sudden drops.</li>"
        "<li>Weather disruptions reduce orders.</li>"
        "</ul>"
    )


# ═══════════════════════════════════════════════════════════════════════
#  PAGE 4: PRODUCT DEMAND SEGMENTS
# ═══════════════════════════════════════════════════════════════════════
elif page == "4. Product Demand Segments":
    st.markdown("## 📦 Product Demand Segments")
    st.caption("Categorizing products using K-Means Clustering to drive stocking strategies.")
    st.divider()

    if os.path.exists("task6_clusters.csv"):
        cluster_df = pd.read_csv("task6_clusters.csv")
        
        total_sub_categories = cluster_df.shape[0]
        clusters_created = cluster_df['Business Interpretation'].nunique()
        highest_revenue_cluster = cluster_df.groupby('Business Interpretation')['Total_Sales'].sum().idxmax()
        highest_growth_cluster = cluster_df.groupby('Business Interpretation')['Growth_Rate'].mean().idxmax()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Sub-Categories", total_sub_categories)
        m2.metric("Clusters Created", clusters_created)
        m3.metric("Highest Revenue Cluster", highest_revenue_cluster)
        m4.metric("Highest Growth Cluster", highest_growth_cluster)
        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Elbow Method for Optimal Clusters")
            if os.path.exists("charts/elbow_method.png"):
                st.image("charts/elbow_method.png", width='stretch')
            st.markdown("**Optimal K Selected = 4**")
                
        with c2:
            st.markdown("#### Demand Segments (PCA Reduced)")
            if os.path.exists("charts/product_clusters.png"):
                st.image("charts/product_clusters.png", width='stretch')

        st.divider()
        section_title("📋 Sub-Category Stocking Strategy")
        
        def highlight_clusters(s):
            if s == 'High Volume Stable Demand': return 'background-color: rgba(46, 204, 113, 0.2)'
            elif s == 'Growing Products': return 'background-color: rgba(52, 152, 219, 0.2)'
            elif s == 'Seasonal / Volatile Products': return 'background-color: rgba(230, 126, 34, 0.2)'
            elif s == 'Low Demand Products': return 'background-color: rgba(231, 76, 60, 0.2)'
            return ''

        try:
            styled_df = cluster_df.style.map(highlight_clusters, subset=['Business Interpretation'])
        except AttributeError:
            styled_df = cluster_df.style.applymap(highlight_clusters, subset=['Business Interpretation'])

        st.dataframe(styled_df, width='stretch', hide_index=True)
        
        insight_html(
            "<strong>High Volume Stable Demand:</strong> Products that generate consistent revenue. Never stock out.<br>"
            "<strong>Growing Products:</strong> Products gaining traction. Incrementally increase orders.<br>"
            "<strong>Seasonal / Volatile:</strong> Unpredictable or seasonal demand. Time orders tightly with peaks.<br>"
            "<strong>Low Demand:</strong> Minimal contribution. Avoid heavy warehousing."
        )
