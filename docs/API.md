# DQML API Documentation

## Overview

The DQML API provides a RESTful interface for executing Data Mining Query Language queries. The API is built with FastAPI and supports query execution, data loading, and health monitoring.

**Base URL:** `http://localhost:8000`

---

## Endpoints

### Execute Query

Execute a DMQL query and return results with optional mining analysis and visualization.

**Endpoint:** `POST /api/execute`

**Content-Type:** `application/json`

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | The DMQL query to execute |
| `data` | object | No | Optional inline data as key-value pairs |

#### Example Request

```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "FROM customers WHERE age > 30"}'
```

#### Response

```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Bob", "age": 35, "income": 75000},
    {"id": 2, "name": "Carol", "age": 45, "income": 90000}
  ],
  "columns": ["id", "name", "age", "income"],
  "row_count": 2,
  "mining_result": null,
  "chart": null,
  "sql": "SELECT * FROM customers WHERE age > 30",
  "error": null,
  "query_type": "select"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the query executed successfully |
| `data` | array | Array of result rows as objects |
| `columns` | array | Column names in the result |
| `row_count` | integer | Number of rows returned |
| `mining_result` | object | Mining operation results (if applicable) |
| `chart` | object | Plotly chart data (if visualization requested) |
| `sql` | string | The SQL query that was executed |
| `error` | string | Error message if execution failed |
| `query_type` | string | Type of query: "select" or "mining" |

---

### Mining Query Example

```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "FROM customers MINE CLUSTER K=3"}'
```

#### Mining Response

```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Alice", "age": 25, "income": 50000, "cluster": 0},
    {"id": 2, "name": "Bob", "age": 35, "income": 75000, "cluster": 1}
  ],
  "columns": ["id", "name", "age", "income", "cluster"],
  "row_count": 10,
  "mining_result": {
    "type": "clustering",
    "method": "kmeans",
    "n_clusters": 3,
    "inertia": 12345.67,
    "cluster_sizes": [3, 4, 3]
  },
  "chart": {
    "data": [...],
    "layout": {...}
  },
  "query_type": "mining"
}
```

---

### Load CSV Data

Load a CSV file into the database for querying.

**Endpoint:** `POST /api/load-csv`

**Content-Type:** `application/json`

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file_path` | string | Yes | Absolute path to the CSV file |
| `table_name` | string | Yes | Name for the table in the database |

#### Example Request

```bash
curl -X POST http://localhost:8000/api/load-csv \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/data/customers.csv", "table_name": "customers"}'
```

#### Response

```json
{
  "success": true,
  "table_name": "customers",
  "row_count": 100,
  "columns": ["id", "name", "age", "income", "region"],
  "error": null
}
```

---

### List Tables

Get a list of all tables loaded in the database.

**Endpoint:** `GET /api/tables`

#### Example Request

```bash
curl http://localhost:8000/api/tables
```

#### Response

```json
{
  "tables": ["customers", "transactions", "products"]
}
```

---

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

#### Example Request

```bash
curl http://localhost:8000/api/health
```

#### Response

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Mining Results

### Clustering Result

When using `MINE CLUSTER K=n`:

```json
{
  "type": "clustering",
  "method": "kmeans",
  "n_clusters": 3,
  "inertia": 12345.67,
  "cluster_sizes": [10, 15, 25]
}
```

### Statistics Result

When using `MINE STATISTICS`:

```json
{
  "type": "statistics",
  "summary": {
    "age": {
      "count": 100,
      "mean": 35.5,
      "std": 12.3,
      "min": 18,
      "25%": 25,
      "50%": 35,
      "75%": 45,
      "max": 65
    }
  },
  "profile": {
    "total_rows": 100,
    "total_columns": 5,
    "numeric_columns": 3,
    "categorical_columns": 2
  }
}
```

### Anomaly Detection Result

When using `MINE ANOMALIES`:

```json
{
  "type": "anomaly_detection",
  "method": "isolation_forest",
  "n_anomalies": 5,
  "anomaly_ratio": 0.05,
  "anomaly_indices": [12, 45, 67, 89, 92]
}
```

---

## Chart Data Format

Chart data is returned in Plotly format for direct rendering:

```json
{
  "data": [
    {
      "type": "scatter",
      "x": [1, 2, 3, 4, 5],
      "y": [10, 20, 15, 25, 30],
      "mode": "markers",
      "marker": {"color": [0, 1, 0, 2, 1]}
    }
  ],
  "layout": {
    "title": "Clustering Results",
    "xaxis": {"title": "Feature 1"},
    "yaxis": {"title": "Feature 2"}
  }
}
```

---

## Error Handling

### Error Response

```json
{
  "success": false,
  "data": null,
  "columns": null,
  "row_count": 0,
  "mining_result": null,
  "chart": null,
  "sql": null,
  "error": "Error message describing what went wrong",
  "query_type": null
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid query syntax) |
| 404 | Not Found (file not found for CSV loading) |
| 422 | Validation Error (invalid request body) |
| 500 | Internal Server Error |

---

## CORS Configuration

The API allows cross-origin requests from the following origins:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## Authentication

The API currently does not require authentication. For production deployment, implement appropriate authentication mechanisms.
