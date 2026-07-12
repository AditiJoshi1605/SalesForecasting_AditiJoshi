# 📊 End-to-End Sales Forecasting & Demand Intelligence System

**Internship Project | Superstore Sales Dataset**

A fully interactive, multi-page Streamlit dashboard built to analyze historical sales patterns, forecast future demand, detect anomalies, and segment products by demand behavior.

---

## 🚀 Live Dashboard

👉 [Click here to view the live app](#) *(replace with your Streamlit Cloud URL after deployment)*

---

## 📁 Project Structure

```
SalesForecasting/
├── app.py                    # Main Streamlit dashboard (4-page layout)
├── analysis.ipynb            # Full analysis notebook (Tasks 1–7)
├── requirements.txt          # All Python dependencies
├── summary.pdf               # Executive Business Report (Task 8)
├── train.csv                 # Superstore sales dataset
├── vgsales.csv               # Supplementary dataset (Video Game Sales)
├── model_comparison.csv      # MAE, RMSE, MAPE for SARIMA, Prophet, XGBoost
├── task4_forecasts.csv       # 3-month forecasts for 3 categories + 4 regions
├── task6_clusters.csv        # K-Means cluster labels & stocking strategies
├── anomalies.csv             # Detected anomaly dates, types & reasons
└── charts/                   # All pre-generated chart images (14 PNGs)
```

---

## 🧠 Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| Task 1 | Data Loading & EDA | ✅ |
| Task 2 | Time Series Analysis (Decomposition, ADF Test) | ✅ |
| Task 3 | Forecasting Models: SARIMA, Prophet, XGBoost | ✅ |
| Task 4 | Category & Region-Level Forecasting | ✅ |
| Task 5 | Anomaly Detection (Isolation Forest + Z-Score) | ✅ |
| Task 6 | Product Demand Segmentation (K-Means Clustering) | ✅ |
| Task 7 | 4-Page Interactive Streamlit Dashboard | ✅ |
| Task 8 | Executive Business Report (`summary.pdf`) | ✅ |

---

## 📊 Dashboard Pages

1. **Sales Overview** — Business KPIs, filters (Category / Region / Year), Sales by Year bar chart, Monthly Trend, Business Insights
2. **Forecast Explorer** — Model comparison (MAE, RMSE, MAPE), forecast charts, category & region forecast horizon viewer
3. **Anomaly Report** — KPI summary, Anomaly Log table, Isolation Forest vs Z-Score comparison, supplementary dataset validation
4. **Product Demand Segments** — K-Means clusters, PCA visualization, color-coded stocking strategy table

---

## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Dependencies

| Package | Version |
|---------|---------|
| streamlit | 1.59.1 |
| pandas | 2.3.0 |
| numpy | 1.26.4 |
| scikit-learn | 1.6.0 |
| xgboost | 3.2.0 |
| matplotlib | 3.10.0 |
| seaborn | 0.13.2 |
| statsmodels | 0.14.6 |
| prophet | 1.3.0 |
| Pillow | 11.0.0 |

---

## 👩‍💻 Author

**Aditi Joshi** — Data Science Intern
