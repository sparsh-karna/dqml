# DQML - Data Mining Query Language

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/React-18.2-61DAFB.svg" alt="React 18.2">
  <img src="https://img.shields.io/badge/FastAPI-0.109-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/ANTLR4-4.13-red.svg" alt="ANTLR4">
  <img src="https://img.shields.io/badge/tests-108%20passing-brightgreen.svg" alt="Tests">
</p>

**DQML** is a domain-specific query language that extends SQL with built-in data mining capabilities. Write familiar SQL-like queries enhanced with clustering, statistical analysis, anomaly detection, and automatic visualization generation.

## 🚀 Features

- **SQL-Like Syntax**: Familiar query structure with `SELECT`, `FROM`, `WHERE` clauses
- **Built-in Data Mining**: K-Means clustering, DBSCAN, statistical analysis, anomaly detection
- **Auto-Visualization**: Generate Plotly charts directly from query results
- **ANTLR4 Parser**: Robust grammar-based query parsing
- **REST API**: FastAPI backend for easy integration
- **React Frontend**: Monaco editor-based query interface with live results

## 📋 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- ANTLR4 (for grammar regeneration)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dqml.git
cd dqml

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..
```

### Running the Application

```bash
# Terminal 1: Start backend
source venv/bin/activate
uvicorn backend.api.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## 📖 DMQL Query Examples

### Basic SELECT Queries

```sql
-- Select all customers
FROM customers

-- Filter with WHERE clause
FROM customers WHERE age > 30

-- Select from transactions
SELECT * FROM transactions WHERE amount > 100
```

### Data Mining Operations

```sql
-- K-Means clustering with 3 clusters
FROM customers MINE CLUSTER K=3

-- K-Means with custom cluster count
FROM transactions MINE CLUSTER K=5

-- Basic statistics
FROM transactions MINE STATISTICS

-- Anomaly detection
FROM transactions MINE ANOMALIES
```

### Visualization

```sql
-- Display as bar chart
SELECT category, amount FROM transactions DISPLAY AS bar

-- Scatter plot
FROM customers MINE CLUSTER K=3 DISPLAY AS scatter

-- Heatmap for correlations
FROM transactions MINE STATISTICS DISPLAY AS heatmap
```

## 🏗️ Architecture

```
dqml/
├── backend/
│   ├── api/                 # FastAPI REST API
│   │   └── main.py
│   ├── dqml/
│   │   ├── parser/          # ANTLR4 grammar & parser
│   │   │   ├── DMQL.g4
│   │   │   └── dmql_parser.py
│   │   ├── executor/        # SQLite query executor
│   │   ├── mining/          # Data mining operations
│   │   │   ├── clustering.py
│   │   │   ├── statistics.py
│   │   │   └── anomaly_detection.py
│   │   └── visualization/   # Plotly chart generation
│   └── tests/               # 108 tests
├── frontend/
│   └── src/
│       └── App.tsx          # React UI with Monaco editor
└── requirements.txt
```

## 🧪 Testing

```bash
# Run all tests (108 tests)
cd /path/to/dqml
source venv/bin/activate
PYTHONPATH=backend pytest backend/tests/ -v

# Run specific test modules
pytest backend/tests/test_parser.py -v      # Parser tests (22)
pytest backend/tests/test_mining.py -v      # Mining tests (9)
pytest backend/tests/test_visualization.py -v  # Visualization tests (28)
pytest backend/tests/test_api.py -v         # API tests (13)
pytest backend/tests/test_integration.py -v # Integration tests (17)
```

## 📚 API Reference

### POST /api/execute

Execute a DMQL query.

**Request:**
```json
{
  "query": "FROM customers MINE CLUSTER K=3"
}
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "columns": ["id", "name", "age", "cluster"],
  "row_count": 10,
  "mining_result": {
    "type": "clustering",
    "n_clusters": 3,
    "cluster_sizes": [3, 4, 3]
  },
  "chart": {
    "data": [...],
    "layout": {...}
  },
  "query_type": "mining"
}
```

### POST /api/load-csv

Load a CSV file into the database.

**Request:**
```json
{
  "file_path": "/path/to/data.csv",
  "table_name": "my_table"
}
```

### GET /api/tables

List all loaded tables.

### GET /api/health

Health check endpoint.

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| Parser | ANTLR4 4.13.1 |
| Backend | Python 3.9+, FastAPI, SQLite |
| Mining | scikit-learn (K-Means, Isolation Forest) |
| Visualization | Plotly |
| Frontend | React 18, TypeScript, Vite |
| Editor | Monaco Editor |

## 📝 DMQL Grammar

The DMQL grammar extends SQL with mining and visualization clauses:

```antlr
query
    : (useClause)?
      (selectClause)?
      fromClause
      (whereClause)?
      (mineClause)?
      (displayClause)?
      EOF
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
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ANTLR4](https://www.antlr.org/) for the parser generator
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent REST framework
- [Plotly](https://plotly.com/) for interactive visualizations
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) for the code editor
- [scikit-learn](https://scikit-learn.org/) for machine learning algorithms
