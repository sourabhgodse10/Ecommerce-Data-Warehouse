# E-Commerce Data Warehouse & Analytics Project

A comprehensive data engineering project demonstrating ETL pipelines, data warehousing, and analytics using real-world e-commerce data.

## 📊 Project Overview

This project builds a dimensional data warehouse from raw e-commerce transaction data (Amazon Sales Dataset), including:
- **Data Extraction**: Download from Kaggle using API
- **Data Transformation**: ETL pipeline with Python/Pandas/NumPy
- **Data Loading**: Create fact and dimension tables
- **Analytics**: Business intelligence queries and visualizations
- **Documentation**: Jupyter notebooks with exploratory data analysis

### Skills Demonstrated
- ✅ Python, Pandas, NumPy
- ✅ Scikit-learn (data preprocessing, clustering)
- ✅ SQL & Data Warehousing concepts (fact tables, dimensions)
- ✅ ETL/Data Pipeline Development
- ✅ Exploratory Data Analysis (EDA)
- ✅ Data Visualization
- ✅ Business Intelligence & Reporting

## 📁 Project Structure

```
ecommerce-data-warehouse/
├── data/
│   ├── raw/                 # Raw data from Kaggle
│   └── processed/           # Cleaned and transformed data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_etl_pipeline.ipynb
│   ├── 03_warehouse_schema.ipynb
│   └── 04_analytics_insights.ipynb
├── scripts/
│   ├── download_data.py     # Download Amazon dataset from Kaggle
│   ├── etl_pipeline.py      # ETL transformation logic
│   └── queries.py           # Analytics queries
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Kaggle account (free)
- Kaggle API credentials

### 1. Setup Kaggle API

```bash
# Create a Kaggle account: https://www.kaggle.com
# Go to Account settings → API → Create New API Token
# This downloads kaggle.json

# Place it in the correct location:
# Windows: C:\Users\<YourUsername>\.kaggle\kaggle.json
# Linux/Mac: ~/.kaggle/kaggle.json

# Set permissions (Linux/Mac only):
chmod 600 ~/.kaggle/kaggle.json
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Dataset

```bash
python scripts/download_data.py
```

This will download the Amazon Sales dataset (~50-100MB) to `data/raw/`

### 4. Run ETL Pipeline

```bash
python scripts/etl_pipeline.py
```

This processes raw data and creates transformed tables in `data/processed/`

### 5. Explore Notebooks

Open Jupyter and explore:
1. **01_data_exploration.ipynb** - Data overview, statistics, distributions
2. **02_etl_pipeline.ipynb** - Step-by-step transformation process
3. **03_warehouse_schema.ipynb** - Dimensional model and fact tables
4. **04_analytics_insights.ipynb** - Business intelligence queries and visualizations

## 📊 Dataset Overview

**Amazon Sales Dataset** includes:
- **Sales Records**: 1000+ transactions with amounts, dates, quantities
- **Product Info**: Categories, subcategories, pricing, ratings
- **Geographic Data**: Countries, regions, shipping information
- **Time Dimensions**: Dates, quarters, years for trend analysis
- **Metrics**: Revenue, profit, discount impact, customer segments

## 🔄 Data Pipeline Architecture

```
Raw CSV Data
    ↓
[Load into Pandas DataFrames]
    ↓
[Data Quality Checks & Cleansing]
    ↓
[Feature Engineering & Aggregations]
    ↓
[Create Dimensional Model]
    ↓
Fact Table (Sales)
├── Dimension: Products
├── Dimension: Customers/Regions
├── Dimension: Dates
└── Dimension: Categories
    ↓
[Analytics Queries & Visualization]
```

## 📈 Key Analytics Delivered

1. **Revenue Analysis**
   - Total sales by category, region, and time period
   - Revenue trends and seasonality

2. **Product Performance**
   - Top products by revenue and quantity sold
   - Profit margins by category
   - Product ratings correlation with sales

3. **Geographic Insights**
   - Sales by country and region
   - Regional profitability analysis

4. **Customer Segmentation**
   - Customer value analysis
   - Purchase frequency and patterns

5. **Forecasting** (bonus)
   - Time series forecasting using Scikit-learn
   - Trend analysis

## 🛠 Technologies Used

| Category | Tools |
|----------|-------|
| **Data Processing** | Pandas, NumPy |
| **ML/Statistics** | Scikit-learn, SciPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Data Source** | Kaggle API |
| **Documentation** | Jupyter Notebooks |
| **Version Control** | Git/GitHub |

## 📝 Jupyter Notebooks Overview

### 01_data_exploration.ipynb
- Load and inspect raw data
- Statistical summaries (mean, median, std dev)
- Missing value analysis
- Data type validation
- Distribution analysis

### 02_etl_pipeline.ipynb
- Data quality checks
- Handling null values
- Outlier detection using NumPy
- Feature engineering with Pandas
- Data aggregations and pivots

### 03_warehouse_schema.ipynb
- Dimensional modeling concepts
- Creating fact table (Sales)
- Creating dimension tables (Products, Geography, Time)
- Surrogate keys and relationships
- Star schema diagram

### 04_analytics_insights.ipynb
- Business intelligence queries
- Revenue and profit analysis
- Trend analysis and time series
- Customer segmentation using Scikit-learn
- Interactive visualizations
- Export results for reporting

## 🎓 Learning Outcomes

By completing this project, you demonstrate:

✅ **Data Engineering**: ETL pipeline development, data validation, schema design  
✅ **Python Mastery**: Pandas operations, NumPy calculations, data manipulation  
✅ **Analytics**: SQL-like queries using Pandas, aggregations, groupby operations  
✅ **ML Skills**: Scikit-learn preprocessing, clustering, feature scaling  
✅ **Documentation**: Clear README, notebook explanations, code comments  
✅ **Problem-Solving**: Handling missing data, outliers, data quality issues  
✅ **Visualization**: Creating insights-driven plots and dashboards  

## 📚 Resume Talking Points

- "Built end-to-end ETL pipeline processing 50k+ records using Python/Pandas"
- "Designed dimensional data warehouse with fact and dimension tables"
- "Performed exploratory data analysis revealing key business insights"
- "Automated data download and transformation using Python scripts"
- "Created analytical dashboards for C-level reporting"

## 🔗 Useful Resources

- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Scikit-learn Tutorials](https://scikit-learn.org/stable/documentation.html)

## 📄 License

This project uses publicly available datasets for educational purposes.

---

**Author**: Your Name  
**Last Updated**: March 2026  
**Status**: Complete MVP
