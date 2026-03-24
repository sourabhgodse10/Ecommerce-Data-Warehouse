#!/usr/bin/env python3
"""
ETL Pipeline for E-Commerce Data Warehouse

Transforms raw data into dimensional model:
- Fact Table: Sales transactions
- Dimension Tables: Products, Geography, Dates, Categories
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.preprocessing import StandardScaler

class EcommerceDWPipeline:
    """ETL Pipeline for E-Commerce Data Warehouse"""
    
    def __init__(self):
        self.raw_path = Path(__file__).parent.parent / 'data' / 'raw'
        self.processed_path = Path(__file__).parent.parent / 'data' / 'processed'
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        self.raw_data = {}
        self.processed_data = {}
    
    def load_raw_data(self):
        """Load raw CSV files into DataFrames"""
        print("\n📂 Loading raw data...")
        
        try:
            # Find all CSV files
            csv_files = list(self.raw_path.glob('*.csv'))
            if not csv_files:
                print(f"❌ No CSV files found in {self.raw_path}")
                return False
            
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    self.raw_data[csv_file.stem] = df
                    print(f"   ✅ {csv_file.name}: {len(df):,} rows, {len(df.columns)} columns")
                except Exception as e:
                    print(f"   ⚠️  {csv_file.name}: {e}")
            
            return len(self.raw_data) > 0
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def data_quality_checks(self):
        """Validate and report on data quality"""
        print("\n🔍 Data Quality Checks...")
        
        for name, df in self.raw_data.items():
            print(f"\n   📊 {name}:")
            print(f"      Shape: {df.shape}")
            print(f"      Null values: {df.isnull().sum().sum()}")
            print(f"      Duplicates: {df.duplicated().sum()}")
            
            # Show column info
            print(f"      Columns: {list(df.columns)}")
    
    def transform_sales_data(self):
        """Transform raw sales data into fact table"""
        print("\n🔄 Transforming sales data...")
        
        # Get the main sales dataset (usually the first or largest table)
        sales_df = None
        for name, df in self.raw_data.items():
            if 'amount' in df.columns.str.lower() or 'sales' in name.lower():
                sales_df = df.copy()
                break
        
        if sales_df is None:
            # Fallback: use the first dataframe
            sales_df = list(self.raw_data.values())[0].copy()
        
        print(f"   Processing {len(sales_df):,} sales records...")
        
        # Handle missing values
        numeric_cols = sales_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            sales_df[col].fillna(sales_df[col].median(), inplace=True)
        
        # Convert date columns
        date_cols = sales_df.select_dtypes(include=['object']).columns
        for col in date_cols:
            try:
                sales_df[col] = pd.to_datetime(sales_df[col], errors='coerce')
            except:
                pass
        
        # Add calculated fields
        if 'Quantity' in sales_df.columns and 'Amount' in sales_df.columns:
            sales_df['Unit_Price'] = sales_df['Amount'] / sales_df['Quantity']
        
        self.processed_data['fact_sales'] = sales_df
        print(f"   ✅ Created fact_sales with {len(sales_df):,} records")
        
        return sales_df
    
    def create_dimension_tables(self, sales_df):
        """Create dimension tables from sales data"""
        print("\n📦 Creating dimension tables...")
        
        # Dimension: Date
        if any(sales_df.dtypes == 'datetime64[ns]'):
            date_cols = sales_df.select_dtypes(include=['datetime64[ns]']).columns
            date_col = date_cols[0]
            
            dim_date = sales_df[date_col].dt.date.unique()
            dim_date = pd.DataFrame({
                'date_id': range(1, len(dim_date) + 1),
                'date': dim_date,
                'year': pd.to_datetime(dim_date).year,
                'month': pd.to_datetime(dim_date).month,
                'quarter': pd.to_datetime(dim_date).quarter,
            })
            self.processed_data['dim_date'] = dim_date
            print(f"   ✅ dim_date: {len(dim_date)} records")
        
        # Dimension: Products (if available)
        if 'Product' in sales_df.columns or 'Category' in sales_df.columns:
            product_cols = [col for col in sales_df.columns if 'product' in col.lower() or 'category' in col.lower()]
            if product_cols:
                dim_product = sales_df[product_cols].drop_duplicates().reset_index(drop=True)
                dim_product.insert(0, 'product_id', range(1, len(dim_product) + 1))
                self.processed_data['dim_product'] = dim_product
                print(f"   ✅ dim_product: {len(dim_product)} unique products")
        
        # Dimension: Geography (if available)
        if 'Country' in sales_df.columns or 'Region' in sales_df.columns:
            geo_cols = [col for col in sales_df.columns if 'country' in col.lower() or 'region' in col.lower()]
            if geo_cols:
                dim_geo = sales_df[geo_cols].drop_duplicates().reset_index(drop=True)
                dim_geo.insert(0, 'geo_id', range(1, len(dim_geo) + 1))
                self.processed_data['dim_geography'] = dim_geo
                print(f"   ✅ dim_geography: {len(dim_geo)} unique locations")
    
    def aggregate_metrics(self):
        """Create aggregated metric tables"""
        print("\n📊 Creating metric tables...")
        
        sales_df = self.processed_data.get('fact_sales')
        if sales_df is None:
            return
        
        # Overall metrics
        metrics = {
            'Total Records': len(sales_df),
            'Average Amount': sales_df[['Amount']].select_dtypes(include=[np.number]).mean().values[0] if 'Amount' in sales_df.columns else 0,
        }
        
        metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
        self.processed_data['metrics_summary'] = metrics_df
        print(f"   ✅ Created metrics summary")
    
    def save_processed_data(self):
        """Save all processed DataFrames to CSV"""
        print("\n💾 Saving processed data...")
        
        for name, df in self.processed_data.items():
            filepath = self.processed_path / f'{name}.csv'
            df.to_csv(filepath, index=False)
            size_kb = filepath.stat().st_size / 1024
            print(f"   ✅ {name}.csv ({size_kb:.1f} KB)")
    
    def run_pipeline(self):
        """Execute the complete ETL pipeline"""
        print("\n" + "=" * 60)
        print("🚀 E-Commerce Data Warehouse - ETL Pipeline")
        print("=" * 60)
        
        # Step 1: Load
        if not self.load_raw_data():
            print("\n❌ Failed to load raw data. Exiting.")
            return False
        
        # Step 2: Quality checks
        self.data_quality_checks()
        
        # Step 3: Transform
        sales_df = self.transform_sales_data()
        
        # Step 4: Create dimensions
        self.create_dimension_tables(sales_df)
        
        # Step 5: Aggregate
        self.aggregate_metrics()
        
        # Step 6: Save
        self.save_processed_data()
        
        print("\n" + "=" * 60)
        print("✅ Pipeline completed successfully!")
        print("=" * 60)
        print(f"\n📁 Processed data saved to: {self.processed_path}")
        print("\nNext steps:")
        print("   1. Review 03_warehouse_schema.ipynb for schema details")
        print("   2. Run 04_analytics_insights.ipynb for analysis")
        
        return True


if __name__ == '__main__':
    pipeline = EcommerceDWPipeline()
    pipeline.run_pipeline()
