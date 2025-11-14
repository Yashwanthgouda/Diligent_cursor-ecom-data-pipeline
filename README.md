# Diligent Cursor E-Commerce Data Pipeline

## Project Prompt

> I want you to perform an end-to-end data engineering workflow inside this Cursor workspace. Please complete ALL tasks exactly as described below:  
>  
> **TASK 1: PUSH CODE TO GITHUB**  
> 1. Initialize git in this project.  
> 2. Create a new GitHub repository named "Diligent_cursor-ecom-data-pipeline".  
> 3. Add all project files, commit them, set the remote origin, and push to GitHub.  
> 4. Confirm the push was successful.  
>  
> **TASK 2: GENERATE SYNTHETIC DATA**  
> Create a folder named "data" and inside it generate the following 5 CSV files with realistic synthetic e-commerce data. Ensure referential integrity between tables.  
> 1. customers.csv (customer_id, name, age, gender, location, signup_date) – 500 rows  
> 2. products.csv (product_id, name, category, price, brand) – 200 rows  
> 3. orders.csv (order_id, customer_id, order_date, total_amount, payment_method) – 1000 rows  
> 4. order_items.csv (item_id, order_id, product_id, quantity, item_price) – 2000 rows  
> 5. reviews.csv (review_id, customer_id, product_id, rating, review_text, review_date) – 300 rows  
> Requirements: valid dates, realistic prices, varied categorical values, and correct FK relationships.  
>  
> **TASK 3: CREATE PYTHON INGESTION PIPELINE**  
> Write `ingest_data.py` that creates `ecommerce.db`, builds tables for all datasets, loads CSVs with pandas, and writes them via `to_sql(if_exists="replace")`, then prints row counts.  
>  
> **TASK 4: WRITE COMPLEX SQL QUERY**  
> Create `report.sql` with a customer spending report query joining customers → orders → order_items → products. Output: customer_id, customer_name, total_orders, total_items, total_spent, last_order_date. Order by total_spent DESC.  
>  
> **FINAL REQUIREMENT**  
> Verify CSVs, database, ingestion script, and query; then push final code to GitHub.

## Repository Overview

This repo delivers a miniature data engineering workflow for an e-commerce scenario:

- **Synthetic Data Generation** – `generate_data.py` creates five CSVs with realistic values and referential integrity under `data/`.
- **SQLite Ingestion Pipeline** – `ingest_data.py` loads the CSVs with pandas, writes them into `ecommerce.db`, and prints row counts for verification.
- **Analytics Query** – `report.sql` contains the requested customer spending report using joins across customers, orders, order_items, and products.

## Project Structure

```
.
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── reviews.csv
├── ecommerce.db
├── generate_data.py
├── ingest_data.py
├── report.sql
└── README.md
```

## Environment Setup

1. **Install Dependencies**
   ```bash
   pip install pandas numpy
   ```

2. **Generate Synthetic Data**
   ```bash
   python generate_data.py
   ```
   This populates all CSVs under `data/`.

3. **Ingest into SQLite**
   ```bash
   python ingest_data.py
   ```
   The script creates/overwrites `ecommerce.db` and prints table row counts.

4. **Validate SQL Report**
   Run the query inside `report.sql` against the SQLite database, for example:
   ```bash
   python - <<'PY'
   import sqlite3, pathlib
   sql = pathlib.Path('report.sql').read_text()
   conn = sqlite3.connect('ecommerce.db')
   rows = conn.execute(sql).fetchmany(5)
   print(rows)
   PY
   ```

## Data Details

- **customers** – demographic info plus signup date between 2020-01-01 and 2024-12-31.
- **products** – realistic categories, brands, and prices ranging \$5–\$500.
- **orders** – assigned to real customers, dates >= signup date, and payment methods (Credit Card, PayPal, Bank Transfer, Apple Pay, Google Pay).
- **order_items** – at least one per order, prices jittered ±10% from base product price; totals roll up to orders.
- **reviews** – random pairings of customers and products with ratings 1–5 and templated feedback text.

## Git Workflow

1. `git init`
2. `git add .`
3. `git commit -m "Initialize data pipeline project"`
4. `git remote add origin https://github.com/Yashwanthgouda/Diligent_cursor-ecom-data-pipeline.git`
5. `git push -u origin master`

> Note: pushing requires credentials with write access to the GitHub repo linked above.

## Verification Checklist

- [x] CSVs generated in `data/`
- [x] `ecommerce.db` created and populated
- [x] `ingest_data.py` prints row counts without errors
- [x] `report.sql` runs successfully against SQLite



