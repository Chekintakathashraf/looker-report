# Getting Started: Complete Beginner's Guide

A step-by-step guide to download, set up, and run the E-Commerce Intelligence Platform on your local machine.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Step 1: Download the Project](#step-1-download-the-project)
3. [Step 2: Install Python & Dependencies](#step-2-install-python--dependencies)
4. [Step 3: Set Up Virtual Environment](#step-3-set-up-virtual-environment)
5. [Step 4: Configure Environment Variables](#step-4-configure-environment-variables)
6. [Step 5: Seed the Database](#step-5-seed-the-database)
7. [Step 6: Run the API Server](#step-6-run-the-api-server)
8. [Step 7: Test the API](#step-7-test-the-api)
9. [Step 8: Connect to Looker Studio](#step-8-connect-to-looker-studio)
10. [Troubleshooting](#troubleshooting)

---

## System Requirements

Before you start, ensure you have:

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.10 or higher
- **Git**: For cloning the repository
- **Terminal/Command Prompt**: To run commands
- **Google Account**: For Google Sheets and Looker Studio (free)
- **Internet Connection**: To download dependencies

### Check Your Python Version

Open your terminal/command prompt and run:

```bash
python --version
```

If you see `Python 3.10.x` or higher, you're good to go. If not, download Python from https://www.python.org/downloads/

---

## Step 1: Download the Project

### Option A: Using Git (Recommended)

If you have Git installed:

```bash
# Clone the repository
git clone https://github.com/your-username/ecommerce_intelligence.git

# Navigate to the project folder
cd ecommerce_intelligence
```

### Option B: Download as ZIP

1. Go to the GitHub repository
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt and navigate to the folder:
   ```bash
   cd path/to/ecommerce_intelligence
   ```

---

## Step 2: Install Python & Dependencies

### On Windows

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check the box "Add Python to PATH"
4. Click "Install Now"

### On macOS

```bash
# Using Homebrew (if installed)
brew install python@3.10

# Or download from https://www.python.org/downloads/
```

### On Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### Verify Installation

```bash
python --version
pip --version
```

---

## Step 3: Set Up Virtual Environment

A virtual environment isolates your project dependencies from your system Python.

### On Windows

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your terminal prompt.

### On macOS/Linux

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt.

---

## Step 4: Configure Environment Variables

### 4.1 Copy the Example Environment File

```bash
cp .env.example .env
```

### 4.2 View the .env File

```bash
cat .env
```

You should see:
```
DATABASE_URL=sqlite:///./ecommerce_intelligence.db
API_PORT=8000
```

**For local development, these defaults work fine. No changes needed.**

---

## Step 5: Install Project Dependencies

With your virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Faker**: Sample data generation
- **python-dotenv**: Environment variable management
- **Alembic**: Database migrations

Wait for installation to complete (may take 1-2 minutes).

---

## Step 6: Seed the Database

Populate the database with sample data:

```bash
python scripts/seed.py
```

You should see output like:
```
Seeding database...
Created 100 customers
Created 500 products
Created 1000 orders
Database seeded successfully!
```

A file `ecommerce_intelligence.db` will be created in your project folder.

---

## Step 7: Run the API Server

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete.
```

**The API is now running locally!**

---

## Step 8: Test the API

### 8.1 Open Swagger UI (Interactive Documentation)

Open your browser and visit:
```
http://127.0.0.1:8000/docs
```

You'll see an interactive interface with all API endpoints. Click any endpoint to test it.

### 8.2 Test Endpoints Using curl

Open a **new terminal** (keep the API server running in the first one) and run:

```bash
# Test 1: Sales Summary
curl "http://127.0.0.1:8000/api/v1/sales/summary"

# Test 2: Top Products
curl "http://127.0.0.1:8000/api/v1/products/top?limit=5"

# Test 3: Revenue by State
curl "http://127.0.0.1:8000/api/v1/revenue/by-state"
```

Each should return JSON data with no errors.

### 8.3 Export Data for Looker Studio

```bash
# Export top customers
curl "http://127.0.0.1:8000/api/v1/customers/top?limit=10" > customers.json

# Export revenue trend
curl "http://127.0.0.1:8000/api/v1/revenue/trend?months=12" > revenue.json

# Export state revenue
curl "http://127.0.0.1:8000/api/v1/revenue/by-state" > state_revenue.json

# View the data
cat customers.json
```

---

## Step 9: Connect to Looker Studio

### 9.1 Create Google Sheets

1. Go to **https://sheets.google.com**
2. Click **+ Create** → **Blank spreadsheet**
3. Name it "E-Commerce Sales Data"

### 9.2 Import Data into Google Sheets

1. Open one of your exported JSON files:
   ```bash
   cat customers.json
   ```

2. Copy the output

3. In Google Sheets:
   - Create column headers matching the JSON keys
   - Paste the data rows

**Example for customers.json:**

| customer_id | name | email | city | state | total_spent | total_orders |
|---|---|---|---|---|---|---|
| 1 | John Doe | john@example.com | Mumbai | Maharashtra | 15000.50 | 5 |
| 2 | Jane Smith | jane@example.com | Bangalore | Karnataka | 12500.75 | 4 |

4. Copy the Google Sheet URL

### 9.3 Connect to Looker Studio

1. Go to **https://looker.google.com/u/0/reporting**
2. Click **Create** → **Report**
3. Click **Create new data source**
4. Select **Google Sheets**
5. Paste your Google Sheet URL
6. Click **Connect**
7. Add widgets (tables, charts, maps)

**For detailed instructions, see USER_MANUAL.md**

---

## Complete Workflow Checklist

- [ ] Python 3.10+ installed
- [ ] Project downloaded/cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables configured (`.env` file)
- [ ] Database seeded (`python scripts/seed.py`)
- [ ] API server running (`uvicorn app.main:app --reload`)
- [ ] Swagger UI accessible at `http://127.0.0.1:8000/docs`
- [ ] API endpoints tested with curl
- [ ] Data exported to JSON files
- [ ] Google Sheets created with data
- [ ] Looker Studio report connected to Google Sheets
- [ ] First visualization created

---

## Project Structure

```
ecommerce_intelligence/
├── app/
│   ├── api/                 # API endpoints
│   ├── models/              # Database models
│   ├── schemas/             # Response schemas
│   ├── services/            # Business logic
│   ├── db/                  # Database configuration
│   ├── core/                # Core settings
│   └── main.py              # FastAPI app entry point
├── scripts/
│   └── seed.py              # Database seeding script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.example             # Example environment file
├── README.md                # Project overview
├── USER_MANUAL.md           # Looker Studio guide
└── GETTING_STARTED.md       # This file
```

---

## API Endpoints Overview

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/api/v1/sales/summary` | Total revenue, profit, orders | KPI scorecard |
| `/api/v1/sales/daily` | Daily revenue trend | Line chart |
| `/api/v1/sales/funnel` | Order status distribution | Funnel chart |
| `/api/v1/products/top` | Top products by revenue | Bar chart |
| `/api/v1/products/categories` | Revenue by category | Pie chart |
| `/api/v1/products/low-stock` | Low inventory alert | Table |
| `/api/v1/customers/segments` | Customer segments (VIP, Regular, etc.) | Bar chart |
| `/api/v1/customers/top` | Top customers by lifetime value | Table |
| `/api/v1/customers/retention` | New vs returning customers | Area chart |
| `/api/v1/revenue/trend` | Monthly revenue & profit | Combo chart |
| `/api/v1/revenue/by-state` | Revenue by Indian state | Geo map |

---

## Troubleshooting

### Issue: "Python not found" or "python: command not found"

**Solution:**
- Ensure Python is installed and added to PATH
- On Windows, restart your terminal after installing Python
- Try `python3` instead of `python`

### Issue: "pip: command not found"

**Solution:**
```bash
python -m pip install --upgrade pip
```

### Issue: "Virtual environment not activating"

**Solution:**
- On Windows: Use `.venv\Scripts\activate` (not `source`)
- On macOS/Linux: Use `source .venv/bin/activate`
- Ensure you're in the project directory

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
- Ensure virtual environment is activated (you should see `(.venv)` in prompt)
- Run `pip install -r requirements.txt` again

### Issue: "Address already in use" when starting API

**Solution:**
```bash
# Kill the process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Issue: "Database is locked" error

**Solution:**
- Close any other instances of the API server
- Delete `ecommerce_intelligence.db` and re-seed:
  ```bash
  rm ecommerce_intelligence.db
  python scripts/seed.py
  ```

### Issue: "No data in Looker Studio"

**Solution:**
- Verify Google Sheet has data in correct columns
- Check column headers match exactly (case-sensitive)
- Refresh the Looker Studio report

---

## Next Steps

1. ✅ Complete all steps above
2. ✅ Explore all 11 API endpoints
3. ✅ Create multiple Google Sheets for different datasets
4. ✅ Build your first Looker Studio dashboard
5. ✅ Experiment with different chart types
6. ✅ Share your report with others

---

## Getting Help

- **API Documentation**: http://127.0.0.1:8000/docs (when server is running)
- **Looker Studio Help**: https://support.google.com/looker-studio
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Project README**: See README.md in the project folder

---

## Quick Reference Commands

```bash
# Activate virtual environment
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Seed database
python scripts/seed.py

# Start API server
uvicorn app.main:app --reload

# Test API endpoint
curl "http://127.0.0.1:8000/api/v1/sales/summary"

# Export data
curl "http://127.0.0.1:8000/api/v1/customers/top" > customers.json

# Deactivate virtual environment
deactivate
```

---

Happy learning! 🚀
