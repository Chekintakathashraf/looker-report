# E-Commerce Sales Intelligence Platform

FastAPI backend powering Looker Studio dashboards for real-time e-commerce sales analytics.  
Uses **Python 3.10+**, **FastAPI**, **SQLAlchemy 2**, **SQLite**, and **Pydantic v2**.

---

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env             # edit .env if needed (defaults work for SQLite)

# 4. Seed the database
python scripts/seed.py

# 5. Run the API server
uvicorn app.main:app --reload
```

API docs available at: http://127.0.0.1:8000/docs

---

## API Endpoints

| # | Method | Endpoint | Looker Studio Use Case |
|---|--------|----------|------------------------|
| 1 | GET | `/api/v1/sales/summary` | Scorecard KPIs — revenue, profit, AOV, order counts |
| 2 | GET | `/api/v1/sales/daily` | Time-series line chart — daily revenue & profit trend |
| 3 | GET | `/api/v1/sales/funnel` | Funnel/donut chart — order status distribution |
| 4 | GET | `/api/v1/products/top` | Horizontal bar chart — top products by revenue |
| 5 | GET | `/api/v1/products/categories` | Pie chart — category revenue share |
| 6 | GET | `/api/v1/products/low-stock` | Table widget — low inventory alert list |
| 7 | GET | `/api/v1/customers/segments` | Grouped bar — VIP / Regular / New / Inactive mix |
| 8 | GET | `/api/v1/customers/top` | Table — top customers by lifetime value |
| 9 | GET | `/api/v1/customers/retention` | Stacked area — new vs returning customers per month |
| 10 | GET | `/api/v1/revenue/trend` | Combo chart — monthly revenue, profit, MoM growth |
| 11 | GET | `/api/v1/revenue/by-state` | Geo map (India) — revenue choropleth by state |

### Query Parameters

| Endpoint | Param | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `/sales/summary` | `start_date` | string (YYYY-MM-DD) | — | Filter start |
| `/sales/summary` | `end_date` | string (YYYY-MM-DD) | — | Filter end |
| `/sales/daily` | `start_date`, `end_date` | string | — | Date range |
| `/products/top` | `limit` | int | 10 | Number of products |
| `/products/top` | `category_id` | int | — | Filter by category |
| `/products/low-stock` | `threshold` | int | 10 | Stock threshold |
| `/customers/top` | `limit` | int | 10 | Number of customers |
| `/revenue/trend` | `months` | int | 12 | Lookback window |

---

## Connecting to Looker Studio

### Option A — Google Sheets Export (recommended for local SQLite)

1. Export any endpoint response to CSV: `curl http://127.0.0.1:8000/api/v1/revenue/trend | python -m json.tool`
2. Paste data into Google Sheets.
3. In Looker Studio, add **Google Sheets** as data source.

### Option B — Expose local API via ngrok

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
# Use the HTTPS forwarding URL as a JSON/CSV connector in Looker Studio
```

### Option C — Deploy to a cloud host (Railway, Render, Fly.io)

Deploy the FastAPI app and point Looker Studio to the public URL using the
**JSON data source** connector (community connector or native fetch).

> **Note**: Looker Studio does not natively connect to SQLite files.  
> For a direct DB connection, migrate to PostgreSQL (swap `DATABASE_URL` in `.env`  
> and add `psycopg2-binary` to `requirements.txt`) and use the native PostgreSQL connector.

---

## Dashboard Ideas for Looker Studio

### 1. Executive Overview
- Scorecard row: total revenue, profit, AOV, delivered orders
- Daily revenue line chart (last 30 days)
- Order funnel donut chart
- *Data sources*: `/sales/summary`, `/sales/daily`, `/sales/funnel`

### 2. Revenue Trend Analysis
- Monthly combo chart: bars for revenue/profit, line for MoM growth %
- YoY comparison table
- *Data source*: `/revenue/trend`

### 3. Product Performance
- Top 10 products horizontal bar (revenue + profit)
- Category revenue pie chart
- Low-stock alert table with conditional red formatting
- *Data sources*: `/products/top`, `/products/categories`, `/products/low-stock`

### 4. Customer Intelligence
- Segment distribution bar chart (VIP / Regular / New / Inactive)
- Top 20 customers table sortable by lifetime value
- New vs returning customers stacked area (12 months)
- *Data sources*: `/customers/segments`, `/customers/top`, `/customers/retention`

### 5. Geo Revenue Map
- India choropleth map coloured by state revenue
- Companion table: state, revenue, orders, customers
- *Data source*: `/revenue/by-state`
