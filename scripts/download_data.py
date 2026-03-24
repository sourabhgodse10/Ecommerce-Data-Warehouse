#!/usr/bin/env python3
"""
Download Amazon Sales Dataset from Kaggle

Requirements:
1. Create Kaggle account: https://www.kaggle.com
2. Go to Account → API → Create New API Token
3. Place kaggle.json in ~/.kaggle/ (Windows: C:\Users\<YourUsername>\.kaggle\)
4. Install kaggle: pip install kaggle
"""

import os
import sys
from pathlib import Path

def setup_kaggle_credentials():
    """Verify Kaggle credentials are set up"""
    home = Path.home()
    kaggle_config = home / '.kaggle' / 'kaggle.json'
    
    if not kaggle_config.exists():
        print("❌ Kaggle credentials not found!")
        print(f"\n📝 Setup Instructions:")
        print("1. Go to https://www.kaggle.com/account/login")
        print("2. Go to Account → Settings → API → Create New API Token")
        print(f"3. Place kaggle.json at: {kaggle_config}")
        print("4. Run this script again")
        sys.exit(1)
    
    print("✅ Kaggle credentials found!")
    return True

def download_dataset():
    """Download Amazon Sales dataset from Kaggle"""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("❌ Kaggle package not installed!")
        print("📦 Install it with: pip install kaggle")
        sys.exit(1)
    
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Create data directory
    raw_data_path = Path(__file__).parent.parent / 'data' / 'raw'
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📥 Downloading Amazon Sales Dataset...")
    print(f"📂 Destination: {raw_data_path}")
    
    try:
        # Download the dataset
        api.dataset_download_files(
            'karkavelrajaj/amazon-sales-dataset',
            path=raw_data_path,
            unzip=True
        )
        print("✅ Download complete!")
        
        # List downloaded files
        files = list(raw_data_path.glob('*.csv'))
        print(f"\n📋 Downloaded files:")
        for f in files:
            size_mb = f.stat().st_size / (1024*1024)
            print(f"   • {f.name} ({size_mb:.2f} MB)")
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Verify Kaggle credentials are correct")
        print("   • Check internet connection")
        print("   • Try again with: python scripts/download_data.py")
        sys.exit(1)

if __name__ == '__main__':
    print("🔄 E-Commerce Data Warehouse - Dataset Downloader")
    print("=" * 50)
    
    # Verify credentials
    setup_kaggle_credentials()
    
    # Download dataset
    download_dataset()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete! Next steps:")
    print("   1. Run ETL pipeline: python scripts/etl_pipeline.py")
    print("   2. Open notebooks: jupyter notebook")
    print("=" * 50)
