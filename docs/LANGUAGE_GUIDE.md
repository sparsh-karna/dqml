# DMQL Language Guide

## Introduction

DMQL (Data Mining Query Language) is a SQL-like declarative language designed specifically for data mining operations. It extends traditional SQL with built-in support for clustering, statistical analysis, anomaly detection, and visualization.

---

## Query Structure

A DMQL query follows this general structure:

```
[USE DATABASE database_name]
[SELECT columns]
FROM table_name
[WHERE conditions]
[MINE operation]
[DISPLAY AS chart_type]
```

### Clause Order

Clauses must appear in this order:
1. `USE DATABASE` (optional)
2. `SELECT` (optional)
3. `FROM` (required)
4. `WHERE` (optional)
5. `MINE` (optional)
6. `DISPLAY AS` (optional)

---

## Clauses

### USE DATABASE Clause

Specify which database context to use.

```sql
USE DATABASE sales_data
```

### SELECT Clause

Specify which columns to retrieve. If omitted, all columns (`*`) are selected.

```sql
SELECT name, age, income FROM customers
SELECT * FROM transactions
```

### FROM Clause

**Required.** Specify the source table.

```sql
FROM customers
FROM transactions
FROM products
```

### WHERE Clause

Filter rows based on conditions.

```sql
FROM customers WHERE age > 30
FROM transactions WHERE amount >= 100 AND category = 'Electronics'
FROM customers WHERE region IN ('North', 'South')
```

#### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal to | `age = 30` |
| `!=`, `<>` | Not equal to | `status != 'inactive'` |
| `>` | Greater than | `amount > 100` |
| `<` | Less than | `age < 25` |
| `>=` | Greater than or equal | `income >= 50000` |
| `<=` | Less than or equal | `score <= 100` |
| `AND` | Logical AND | `age > 25 AND income > 50000` |
| `OR` | Logical OR | `region = 'North' OR region = 'South'` |
| `IN` | Value in list | `category IN ('A', 'B', 'C')` |
| `LIKE` | Pattern matching | `name LIKE 'John%'` |
| `BETWEEN` | Range check | `age BETWEEN 25 AND 45` |

---

## Mining Operations

### CLUSTER

Perform K-Means clustering on numeric columns.

```sql
-- Default K=3
FROM customers MINE CLUSTER

-- Specify number of clusters
FROM customers MINE CLUSTER K=5
FROM transactions MINE CLUSTER K=10
```

**Parameters:**
- `K`: Number of clusters (default: 3)

**Output:**
- Adds a `cluster` column to results
- Returns cluster statistics (sizes, inertia)

### STATISTICS

Calculate descriptive statistics for all numeric columns.

```sql
FROM transactions MINE STATISTICS
FROM customers MINE STATISTICS
```

**Output includes:**
- Count, mean, std, min, max
- Quartiles (25%, 50%, 75%)
- Correlation matrix
- Data profile

### ANOMALIES

Detect outliers using Isolation Forest algorithm.

```sql
FROM transactions MINE ANOMALIES
FROM sensor_data MINE ANOMALIES
```

**Output:**
- Adds `is_anomaly` column (True/False)
- Adds `anomaly_score` column
- Returns count and ratio of anomalies

### ASSOCIATION_RULES

*Note: Association rules mining is defined in the grammar but not yet implemented.*

```sql
FROM transactions MINE ASSOCIATION_RULES
```

---

## Visualization

### DISPLAY AS Clause

Request automatic visualization of query results.

```sql
-- Bar chart
SELECT category, SUM(amount) FROM transactions DISPLAY AS bar

-- Scatter plot
FROM customers MINE CLUSTER K=3 DISPLAY AS scatter

-- Heatmap (correlation matrix)
FROM transactions MINE STATISTICS DISPLAY AS heatmap

-- Line chart
SELECT date, value FROM timeseries DISPLAY AS line

-- Histogram
SELECT age FROM customers DISPLAY AS histogram

-- Box plot
SELECT category, value FROM data DISPLAY AS box

-- Pie chart
SELECT category, COUNT(*) FROM transactions DISPLAY AS pie
```

### Supported Chart Types

| Type | Best For |
|------|----------|
| `bar` | Categorical comparisons |
| `line` | Time series, trends |
| `scatter` | Relationship between variables, clusters |
| `histogram` | Distribution of single variable |
| `heatmap` | Correlation matrices |
| `box` | Distribution comparisons |
| `pie` | Proportions |
| `table` | Raw data display (default) |

---

## Complete Examples

### Example 1: Basic Query

```sql
-- Get all customers
FROM customers

-- Get customers over 30 years old
FROM customers WHERE age > 30

-- Get high-value transactions
FROM transactions WHERE amount > 1000
```

### Example 2: Customer Segmentation

```sql
-- Segment customers into 4 groups based on age and income
FROM customers 
MINE CLUSTER K=4 
DISPLAY AS scatter
```

### Example 3: Transaction Analysis

```sql
-- Analyze transaction patterns
FROM transactions 
MINE STATISTICS 
DISPLAY AS heatmap
```

### Example 4: Fraud Detection

```sql
-- Find anomalous transactions
FROM transactions 
WHERE amount > 0 
MINE ANOMALIES 
DISPLAY AS scatter
```

### Example 5: Combined Query

```sql
-- Analyze North region customers
USE DATABASE sales_db
FROM customers 
WHERE region = 'North' 
MINE CLUSTER K=3 
DISPLAY AS scatter
```

---

## Grammar Reference

The DMQL parser is built using ANTLR4. Here's a simplified grammar:

```antlr
query
    : useClause? selectClause? fromClause whereClause? mineClause? displayClause? EOF
    ;

useClause
    : USE DATABASE IDENTIFIER
    ;

selectClause
    : SELECT (STAR | columnList)
    ;

fromClause
    : FROM IDENTIFIER (COMMA IDENTIFIER)*
    ;

whereClause
    : WHERE condition
    ;

mineClause
    : MINE miningOperation
    ;

miningOperation
    : CLUSTER (K '=' INT)?
    | STATISTICS
    | ANOMALIES
    | ASSOCIATION_RULES
    ;

displayClause
    : DISPLAY AS displayType
    ;

displayType
    : BAR | LINE | SCATTER | HISTOGRAM | HEATMAP | BOX | PIE | TABLE
    ;
```

---

## Best Practices

1. **Start Simple**: Begin with basic `FROM table` queries before adding mining operations

2. **Filter First**: Use `WHERE` clauses to reduce data before mining

3. **Choose Appropriate K**: For clustering, start with K=3 and adjust based on results

4. **Match Visualization**: Choose chart types appropriate for your data:
   - Clusters → scatter
   - Statistics → heatmap
   - Anomalies → scatter
   - Aggregations → bar

5. **Load Data First**: Ensure tables are loaded via `/api/load-csv` before querying

---

## Limitations

- Column projection in SELECT is not yet fully implemented (all columns returned)
- ASSOCIATION_RULES is defined but not implemented
- JOIN operations are not supported
- Subqueries are not supported
- Aggregate functions (SUM, COUNT, AVG) are limited
