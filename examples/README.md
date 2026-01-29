# DQML Examples

This folder contains example scripts demonstrating DQML usage.

## Quick Start Examples

### Python Examples

1. **basic_queries.py** - Simple SELECT and filter queries
2. **clustering_example.py** - Customer segmentation with K-Means
3. **anomaly_detection.py** - Fraud detection example

### Running Examples

```bash
# From project root
source venv/bin/activate
cd examples
python basic_queries.py
```

## Sample Queries

### Basic SELECT

```sql
FROM customers
FROM customers WHERE age > 30
SELECT name, income FROM customers WHERE region = 'North'
```

### Clustering

```sql
FROM customers MINE CLUSTER K=3
FROM customers MINE CLUSTER K=5 DISPLAY AS scatter
```

### Statistics

```sql
FROM transactions MINE STATISTICS
FROM customers MINE STATISTICS DISPLAY AS heatmap
```

### Anomaly Detection

```sql
FROM transactions MINE ANOMALIES
FROM transactions WHERE amount > 0 MINE ANOMALIES DISPLAY AS scatter
```

## Using the API

```python
import requests

# Execute a query
response = requests.post(
    "http://localhost:8000/api/execute",
    json={"query": "FROM customers MINE CLUSTER K=3"}
)
result = response.json()

# Access results
print(f"Success: {result['success']}")
print(f"Rows: {result['row_count']}")
print(f"Clusters: {result['mining_result']['n_clusters']}")
```

## Sample Data

The `data/` folder contains sample CSV files:

- **sample_customers.csv** - Customer demographics data
- **sample_transactions.csv** - Transaction records

Load them using the API:

```bash
curl -X POST http://localhost:8000/api/load-csv \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/data/sample_customers.csv", "table_name": "customers"}'
```
