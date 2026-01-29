# Sample Data for DQML Platform

This directory contains sample datasets for testing DQML queries.

## Datasets

### 1. sample_customers.csv
Customer data with demographics and purchase information.

| Column | Type | Description |
|--------|------|-------------|
| id | int | Customer ID |
| name | str | Customer name |
| age | int | Customer age |
| city | str | City of residence |
| purchase_amount | float | Total purchase amount |

### 2. sample_transactions.csv
Transaction data for market basket analysis.

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | int | Transaction ID |
| customer_id | int | Customer ID (FK) |
| product | str | Product name |
| category | str | Product category |
| amount | float | Transaction amount |
| date | date | Transaction date |

## Usage

Load data into DQML:

```sql
USE DATABASE sales_data
FROM customers
WHERE age > 25
MINE STATISTICS
```
