#!/usr/bin/env python3
"""Quick analysis of the data warehouse"""

import pandas as pd
import numpy as np

# Load processed data
df = pd.read_csv('data/processed/fact_sales.csv')

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

print('\n📂 REVENUE BY CATEGORY\n')
category_revenue = df.groupby('Category')['Amount'].agg(['sum', 'mean', 'count']).round(2)
category_revenue.columns = ['Total Revenue', 'Average', 'Count']
print(category_revenue.sort_values('Total Revenue', ascending=False))

print('\n🌍 REVENUE BY COUNTRY\n')
country_revenue = df.groupby('Country')['Amount'].agg(['sum', 'mean', 'count']).round(2)
country_revenue.columns = ['Total Revenue', 'Average', 'Count']
print(country_revenue.sort_values('Total Revenue', ascending=False))

print('\n👥 REVENUE BY CUSTOMER SEGMENT\n')
segment_revenue = df.groupby('Customer_Segment')['Amount'].agg(['sum', 'mean', 'count']).round(2)
segment_revenue.columns = ['Total Revenue', 'Average', 'Count']
print(segment_revenue.sort_values('Total Revenue', ascending=False))

print('\n🏢 REVENUE BY REGION\n')
region_revenue = df.groupby('Region')['Amount'].agg(['sum', 'mean', 'count']).round(2)
region_revenue.columns = ['Total Revenue', 'Average', 'Count']
print(region_revenue.sort_values('Total Revenue', ascending=False))

print('\n📊 TOP 15 PRODUCTS BY REVENUE\n')
product_revenue = df.groupby('Product_Name')['Amount'].agg(['sum', 'mean', 'count']).round(2)
product_revenue.columns = ['Total Revenue', 'Average', 'Count']
top_prod = product_revenue.sort_values('Total Revenue', ascending=False).head(15)
for i, (product, row) in enumerate(top_prod.iterrows(), 1):
    print(f'{i:2d}. {product:40s} Revenue: ${row["Total Revenue"]:>10,.2f} ({int(row["Count"])} units)')

print('\n📈 STATISTICAL SUMMARY (Numeric Columns)\n')
stats = df[['Amount', 'Profit', 'Quantity']].describe().round(2)
print(stats)

print('\n🔍 DATA QUALITY METRICS\n')
print(f'Total Rows: {len(df):,}')
print(f'Missing Values: {df.isnull().sum().sum()}')
print(f'Duplicate Rows: {df.duplicated().sum()}')
print(f'Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB')

print('\n' + '='*70)
print('✅ DATA WAREHOUSE ANALYSIS COMPLETE!')
print('='*70)
