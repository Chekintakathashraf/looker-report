# User Manual: Connecting E-Commerce Intelligence API to Looker Studio via Google Sheets

## Overview

This guide explains how to export data from your FastAPI backend to Google Sheets and connect it to Looker Studio for creating interactive dashboards and reports.

---

## Why Google Sheets?

- **Looker Studio cannot directly access local databases** (SQLite)
- **Google Sheets acts as a bridge** between your local API and Looker Studio
- **Easy to update**: Simply re-export data and refresh in Looker Studio
- **No authentication required** for basic usage
- **Perfect for learning** Looker Studio features

---

## Prerequisites

1. **API running locally**: `uvicorn app.main:app --reload`
2. **Google Account** (free)
3. **Access to Looker Studio** (free at https://looker.google.com)

---

## Step 1: Export Data from Your API

Your API provides 11 endpoints. Export data from each endpoint you want to visualize.

### 1.1 Start Your API Server

```bash
cd /home/codilar/Ashraf/ecommerce_intelligence
source .venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

### 1.2 Export Data Using curl

Run these commands in a new terminal to export data:

```bash
# Sales Summary (KPIs)
curl "http://127.0.0.1:8000/api/v1/sales/summary" > sales_summary.json

# Daily Sales Trend
curl "http://127.0.0.1:8000/api/v1/sales/daily" > sales_daily.json

# Order Funnel
curl "http://127.0.0.1:8000/api/v1/sales/funnel" > sales_funnel.json

# Top Products
curl "http://127.0.0.1:8000/api/v1/products/top?limit=10" > products_top.json

# Product Categories
curl "http://127.0.0.1:8000/api/v1/products/categories" > products_categories.json

# Low Stock Products
curl "http://127.0.0.1:8000/api/v1/products/low-stock?threshold=10" > products_low_stock.json

# Customer Segments
curl "http://127.0.0.1:8000/api/v1/customers/segments" > customers_segments.json

# Top Customers
curl "http://127.0.0.1:8000/api/v1/customers/top?limit=10" > customers_top.json

# Customer Retention
curl "http://127.0.0.1:8000/api/v1/customers/retention" > customers_retention.json

# Revenue Trend
curl "http://127.0.0.1:8000/api/v1/revenue/trend?months=12" > revenue_trend.json

# Revenue by State (Geo Map)
curl "http://127.0.0.1:8000/api/v1/revenue/by-state" > revenue_by_state.json
```

### 1.3 View the Exported Data

```bash
# View any JSON file
cat sales_summary.json
cat products_top.json
cat revenue_by_state.json
```

---

## Step 2: Create Google Sheets for Each Dataset

### 2.1 Create a New Google Sheet

1. Go to **https://sheets.google.com**
2. Click **+ Create** → **Blank spreadsheet**
3. Name it (e.g., "E-Commerce Sales Data")

### 2.2 Import JSON Data into Google Sheets

**Method A: Manual Import (Recommended)**

1. Open your exported JSON file:
   ```bash
   cat products_top.json
   ```

2. The output will look like:
   ```json
   [
     {
       "product_id": 1,
       "product_name": "Laptop",
       "category": "Electronics",
       "total_revenue": 500000.0,
       "total_profit": 100000.0,
       "units_sold": 50
     },
     {
       "product_id": 2,
       "product_name": "Mouse",
       "category": "Accessories",
       "total_revenue": 50000.0,
       "total_profit": 15000.0,
       "units_sold": 500
     }
   ]
   ```

3. In Google Sheets, create column headers matching the JSON keys:
   - A1: `product_id`
   - B1: `product_name`
   - C1: `category`
   - D1: `total_revenue`
   - E1: `total_profit`
   - F1: `units_sold`

4. Manually enter the data rows, or use **Method B** below.

**Method B: Using Google Sheets IMPORTDATA Function**

1. In a blank Google Sheet, cell A1, paste:
   ```
   =IMPORTDATA("https://your-api-url/api/v1/products/top")
   ```

   (Only works if your API is publicly accessible via ngrok or cloud deployment)

**Method C: Copy-Paste from JSON**

1. Open the JSON file in a text editor
2. Copy the data
3. In Google Sheets, use **Data** → **Text to Columns** to parse it

---

## Step 3: Create Separate Sheets for Each Endpoint

Create one Google Sheet with multiple tabs (sheets) for each dataset:

### Sheet Structure Example:

**Sheet 1: Sales Summary**
| total_orders | total_revenue | total_profit | average_order_value | cancelled_orders | delivered_orders |
|---|---|---|---|---|---|
| 1000 | 5000000 | 1250000 | 5000 | 50 | 950 |

**Sheet 2: Top Products**
| product_id | product_name | category | total_revenue | total_profit | units_sold |
|---|---|---|---|---|---|
| 1 | Laptop | Electronics | 500000 | 100000 | 50 |
| 2 | Mouse | Accessories | 50000 | 15000 | 500 |

**Sheet 3: Revenue by State**
| state | total_revenue | total_orders | total_customers |
|---|---|---|---|
| Maharashtra | 2500000 | 1200 | 450 |
| Karnataka | 1800000 | 900 | 320 |

---

## Step 4: Connect Google Sheets to Looker Studio

### 4.1 Create a New Looker Studio Report

1. Go to **https://looker.google.com/u/0/reporting**
2. Click **Create** → **Report**
3. A new blank report opens

### 4.2 Add Data Source (Google Sheet)

1. Click **Create new data source** (top left)
2. Select **Google Sheets**
3. Find and select your Google Sheet
4. Click **Connect**

### 4.3 Add a Table Widget

1. In the report, click **Insert** → **Table**
2. A table appears on the canvas
3. In the **Data** panel (right side), select which columns to display
4. Customize:
   - **Dimensions**: Categorical data (product_name, state, category)
   - **Metrics**: Numerical data (revenue, profit, orders)

---

## Step 5: Create Visualizations

### Example 1: Top Products Table

1. Add a **Table** widget
2. Set **Dimensions**: `product_name`, `category`
3. Set **Metrics**: `total_revenue`, `total_profit`, `units_sold`
4. Sort by `total_revenue` (descending)

### Example 2: Revenue by State (Geo Map)

1. Add a **Geo Chart** widget
2. Set **Location**: `state`
3. Set **Size/Color**: `total_revenue`
4. Looker Studio will automatically color states by revenue

### Example 3: Revenue Trend (Line Chart)

1. Add a **Time Series** chart
2. Set **Date Dimension**: `month`
3. Set **Metric**: `revenue`
4. Shows revenue trend over time

### Example 4: Customer Segments (Bar Chart)

1. Add a **Bar Chart** widget
2. Set **Dimension**: `segment`
3. Set **Metric**: `customer_count`, `total_revenue`
4. Shows segment distribution

---

## Step 6: Refresh Data in Looker Studio

When you update your API data and re-export to Google Sheets:

1. **Update Google Sheet** with new data
2. **In Looker Studio**, click the **Refresh** button (top right)
3. Your visualizations update automatically

---

## Complete Workflow Summary

```
1. Run API Server
   ↓
2. Export Data from Endpoints (curl)
   ↓
3. Create Google Sheets with Exported Data
   ↓
4. Connect Google Sheets to Looker Studio
   ↓
5. Create Tables, Charts, Maps in Looker Studio
   ↓
6. Share Report (optional)
```

---

## API Endpoints Reference

| # | Endpoint | Use Case | Data Type |
|---|----------|----------|-----------|
| 1 | `/api/v1/sales/summary` | KPI Scorecard | Single row |
| 2 | `/api/v1/sales/daily` | Time-series chart | Multiple rows (by date) |
| 3 | `/api/v1/sales/funnel` | Funnel/Donut chart | Multiple rows (by status) |
| 4 | `/api/v1/products/top` | Bar chart | Multiple rows (by product) |
| 5 | `/api/v1/products/categories` | Pie chart | Multiple rows (by category) |
| 6 | `/api/v1/products/low-stock` | Alert table | Multiple rows (low stock items) |
| 7 | `/api/v1/customers/segments` | Segment bar chart | Multiple rows (by segment) |
| 8 | `/api/v1/customers/top` | Customer table | Multiple rows (by customer) |
| 9 | `/api/v1/customers/retention` | Stacked area chart | Multiple rows (by month) |
| 10 | `/api/v1/revenue/trend` | Combo chart | Multiple rows (by month) |
| 11 | `/api/v1/revenue/by-state` | Geo map | Multiple rows (by state) |

---

## Troubleshooting

### Issue: "No data appears in Looker Studio"
- **Solution**: Verify Google Sheet has data in correct columns
- Check that column headers match exactly (case-sensitive)

### Issue: "Geo map not showing states"
- **Solution**: Ensure the state column contains valid Indian state names
- Example valid names: Maharashtra, Karnataka, Tamil Nadu, Delhi, etc.

### Issue: "Charts show no data"
- **Solution**: 
  - Check that metrics are numeric (numbers, not text)
  - Verify dimensions are categorical (text, not numbers)

### Issue: "Google Sheet not connecting to Looker Studio"
- **Solution**:
  - Ensure Google Sheet is shared publicly or with your Google account
  - Check that you're logged into the same Google account in Looker Studio

---

## Learning Resources

- **Looker Studio Help**: https://support.google.com/looker-studio
- **Looker Studio Gallery**: https://lookerstudio.google.com/gallery
- **Your API Documentation**: http://127.0.0.1:8000/docs (when server is running)

---

## Next Steps

1. ✅ Export data from all 11 endpoints
2. ✅ Create Google Sheets for each dataset
3. ✅ Connect to Looker Studio
4. ✅ Create your first dashboard
5. ✅ Experiment with different chart types
6. ✅ Share your report with others

Happy learning with Looker Studio! 🎉
