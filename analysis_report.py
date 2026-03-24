#!/usr/bin/env python3
"""Analysis using raw data from the warehouse"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load raw data
df = pd.read_csv('data/raw/amazon_sales.csv')

print('='*70)
print('📊 E-COMMERCE DATA WAREHOUSE - ANALYSIS RESULTS')
print('='*70)

print('\n💰 REVENUE ANALYSIS\n')
print(f'Total Records: {len(df):,}')
print(f'Total Revenue: ${df["Amount"].sum():,.2f}')
print(f'Average per Transaction: ${df["Amount"].mean():,.2f}')
print(f'Median per Transaction: ${df["Amount"].median():,.2f}')
print(f'Total Profit: ${df["Profit"].sum():,.2f}')
print(f'Profit Margin: {(df["Profit"].sum() / df["Amount"].sum() * 100):.2f}%')
print(f'Profit per Unit Sold: ${(df["Profit"].sum() / df["Quantity"].sum()):.2f}')

print('\n📂 REVENUE BY CATEGORY\n')
category_revenue = df.groupby('Category').agg({
    'Amount': ['sum', 'mean'],
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)
category_revenue.columns = ['Total Revenue', 'Avg Revenue', 'Profit', 'Units Sold']
print(category_revenue.sort_values('Total Revenue', ascending=False))

print('\n🌍 REVENUE BY COUNTRY\n')
country_revenue = df.groupby('Country').agg({
    'Amount': ['sum', 'mean', 'count'],
}).round(2)
country_revenue.columns = ['Total Revenue', 'Average', 'Transactions']
print(country_revenue.sort_values('Total Revenue', ascending=False))

print('\n👥 REVENUE BY CUSTOMER SEGMENT\n')
segment_revenue = df.groupby('Customer_Segment').agg({
    'Amount': ['sum', 'mean', 'count'],
    'Profit': 'sum'
}).round(2)
segment_revenue.columns = ['Total Revenue', 'Average', 'Count', 'Profit']
print(segment_revenue.sort_values('Total Revenue', ascending=False))

print('\n🏢 REVENUE BY REGION\n')
region_revenue = df.groupby('Region').agg({
    'Amount': ['sum', 'mean', 'count'],
}).round(2)
region_revenue.columns = ['Total Revenue', 'Average', 'Transactions']
print(region_revenue.sort_values('Total Revenue', ascending=False))

print('\n📊 TOP 10 PRODUCTS BY REVENUE\n')
product_revenue = df.groupby('Product_Name').agg({
    'Amount': ['sum', 'count'],
    'Profit': 'sum'
}).round(2)
product_revenue.columns = ['Total Revenue', 'Units', 'Profit']
top_prod = product_revenue.sort_values('Total Revenue', ascending=False).head(10)
for i, (product, row) in enumerate(top_prod.iterrows(), 1):
    print(f'{i:2d}. {product:40s} Revenue: ${row["Total Revenue"]:>10,.2f}  Profit: ${row["Profit"]:>10,.2f}')

print('\n📈 PRODUCT SUB-CATEGORIES\n')
subcat_revenue = df.groupby('Sub_Category').agg({
    'Amount': ['sum', 'count'],
}).round(2)
subcat_revenue.columns = ['Total Revenue', 'Transactions']
print(subcat_revenue.sort_values('Total Revenue', ascending=False).head(8))

print('\n📊 STATISTICAL SUMMARY (Numeric Columns)\n')
stats = df[['Amount', 'Profit', 'Quantity']].describe().round(2)
print(stats)

print('\n👥 CUSTOMER SEGMENTATION (K-Means Clustering)\n')
# Prepare data for clustering
numeric_features = df[['Amount', 'Profit', 'Quantity']].copy()
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_features)

# Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(scaled_data)
df['Cluster'] = clusters

print('Cluster Profiles:')
cluster_profiles = df.groupby('Cluster').agg({
    'Amount': 'mean',
    'Profit': 'mean',
    'Quantity': 'mean',
    'Order_Date': 'count'
}).round(2)
cluster_profiles.columns = ['Avg Revenue', 'Avg Profit', 'Avg Quantity', 'Count']
print(cluster_profiles)

print('\nCluster Distribution:')
print(df['Cluster'].value_counts().sort_index())

print('\n🔍 DATA QUALITY METRICS\n')
print(f'Total Rows: {len(df):,}')
print(f'Missing Values: {df.isnull().sum().sum()}')
print(f'Duplicate Rows: {df.duplicated().sum()}')
print(f'Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB')
print(f'Date Range: {df["Order_Date"].min()} to {df["Order_Date"].max()}')

print('\n' + '='*70)
print('✅ DATA WAREHOUSE ANALYSIS COMPLETE!')
print('✅ Project Successfully Executed with Python, Pandas, NumPy & Scikit-learn')
print('='*70)
