#!/usr/bin/env python3
"""
Analytics Queries for E-Commerce Data Warehouse

Demonstrates SQL-like queries using Pandas:
- Revenue analysis
- Customer insights
- Product performance
- Trend analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataWarehouseQueries:
    """SQL-like queries on the data warehouse"""
    
    def __init__(self, data_path):
        self.processed_path = Path(data_path) / 'data' / 'processed'
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load processed data"""
        data_file = self.processed_path / 'cleaned_data.csv'
        self.df = pd.read_csv(data_file)
        print(f"✅ Data loaded: {self.df.shape}")
    
    def query_top_products(self, n=10):
        """Get top products by revenue"""
        product_cols = [col for col in self.df.columns if 'product' in col.lower()]
        amount_cols = [col for col in self.df.columns if 'amount' in col.lower() or 'sales' in col.lower()]
        
        if len(product_cols) == 0 or len(amount_cols) == 0:
            return None
        
        product_col = product_cols[0]
        amount_col = amount_cols[0]
        
        query = self.df.groupby(product_col)[amount_col].agg(['sum', 'count', 'mean']).round(2)
        query.columns = ['Total Revenue', 'Count', 'Average']
        return query.sort_values('Total Revenue', ascending=False).head(n)
    
    def query_revenue_by_category(self):
        """Get revenue by category"""
        cat_cols = [col for col in self.df.columns if 'category' in col.lower()]
        amount_cols = [col for col in self.df.columns if 'amount' in col.lower()]
        
        if len(cat_cols) == 0 or len(amount_cols) == 0:
            return None
        
        cat_col = cat_cols[0]
        amount_col = amount_cols[0]
        
        query = self.df.groupby(cat_col).agg({
            amount_col: ['sum', 'mean', 'count']
        }).round(2)
        query.columns = ['Total Revenue', 'Average', 'Count']
        return query.sort_values('Total Revenue', ascending=False)
    
    def query_geographic_analysis(self):
        """Get revenue by geography"""
        geo_cols = [col for col in self.df.columns if 'country' in col.lower()]
        amount_cols = [col for col in self.df.columns if 'amount' in col.lower()]
        
        if len(geo_cols) == 0 or len(amount_cols) == 0:
            return None
        
        geo_col = geo_cols[0]
        amount_col = amount_cols[0]
        
        query = self.df.groupby(geo_col).agg({
            amount_col: ['sum', 'mean', 'count']
        }).round(2)
        query.columns = ['Total Revenue', 'Average', 'Count']
        return query.sort_values('Total Revenue', ascending=False)
    
    def query_time_series(self):
        """Get daily revenue trend"""
        date_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        amount_cols = [col for col in self.df.columns if 'amount' in col.lower()]
        
        if len(date_cols) == 0 or len(amount_cols) == 0:
            return None
        
        date_col = date_cols[0]
        amount_col = amount_cols[0]
        
        # Convert to datetime if needed
        if self.df[date_col].dtype == 'object':
            self.df[date_col] = pd.to_datetime(self.df[date_col])
        
        query = self.df.groupby(pd.Grouper(key=date_col, freq='D'))[amount_col].agg(['sum', 'count', 'mean']).round(2)
        query.columns = ['Daily Revenue', 'Transaction Count', 'Average']
        return query
    
    def query_high_value_customers(self, threshold_percentile=75):
        """Identify high-value customers"""
        amount_cols = [col for col in self.df.columns if 'amount' in col.lower()]
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower() or 'account' in col.lower()]
        
        if len(amount_cols) == 0:
            return None
        
        amount_col = amount_cols[0]
        threshold = self.df[amount_col].quantile(threshold_percentile / 100)
        
        high_value = self.df[self.df[amount_col] >= threshold]
        return high_value.sort_values(amount_col, ascending=False)
    
    def query_statistics(self):
        """Get overall statistics"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            return None
        
        stats = pd.DataFrame({
            'Mean': self.df[numeric_cols].mean(),
            'Median': self.df[numeric_cols].median(),
            'Std Dev': self.df[numeric_cols].std(),
            'Min': self.df[numeric_cols].min(),
            'Max': self.df[numeric_cols].max(),
            'Q25': self.df[numeric_cols].quantile(0.25),
            'Q75': self.df[numeric_cols].quantile(0.75),
        })
        return stats.round(2)
    
    def run_all_reports(self):
        """Run all analysis queries"""
        print("\n" + "="*60)
        print("📊 E-COMMERCE DATA WAREHOUSE - ANALYTICS REPORTS")
        print("="*60)
        
        # Top Products
        print("\n🏆 TOP 10 PRODUCTS BY REVENUE:")
        print("-" * 60)
        top_products = self.query_top_products()
        if top_products is not None:
            print(top_products)
        
        # Revenue by Category
        print("\n📂 REVENUE BY CATEGORY:")
        print("-" * 60)
        category_revenue = self.query_revenue_by_category()
        if category_revenue is not None:
            print(category_revenue)
        
        # Geographic Analysis
        print("\n🌍 REVENUE BY GEOGRAPHY:")
        print("-" * 60)
        geo_revenue = self.query_geographic_analysis()
        if geo_revenue is not None:
            print(geo_revenue)
        
        # Statistics
        print("\n📊 OVERALL STATISTICS:")
        print("-" * 60)
        stats = self.query_statistics()
        if stats is not None:
            print(stats)
        
        # High Value Customers
        print("\n👑 HIGH-VALUE CUSTOMERS (TOP 75th PERCENTILE):")
        print("-" * 60)
        high_value = self.query_high_value_customers()
        if high_value is not None:
            print(f"Found {len(high_value)} high-value transactions")
            print(high_value.head(10))
        
        print("\n" + "="*60)
        print("✅ All reports completed!")
        print("="*60)


if __name__ == '__main__':
    import sys
    
    # Get project root
    project_root = Path(__file__).parent.parent
    
    try:
        queries = DataWarehouseQueries(project_root)
        queries.run_all_reports()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Installed requirements: pip install -r requirements.txt")
        print("   2. Downloaded data: python scripts/download_data.py")
        print("   3. Run ETL pipeline: python scripts/etl_pipeline.py")
        sys.exit(1)
