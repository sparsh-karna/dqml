# DQML Platform

**Data Mining Query Language Platform** - A modern update to DMQL (1996)

## Overview

DQML (Data Mining Query Language) is a SQL-like declarative language for data mining tasks. This platform provides:

- **Parser**: ANTLR4-based grammar for DQML queries
- **Executor**: Query execution on SQLite/DuckDB
- **Mining**: K-Means clustering, anomaly detection, basic statistics
- **Visualization**: Interactive charts with Plotly

## Quick Start

### Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Generate ANTLR4 parser
cd backend/dqml/parser
antlr4 -Dlanguage=Python3 -visitor DMQL.g4

# Run API server
cd ../../..
python -m uvicorn backend.api.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000

## Sample DQML Queries

```sql
-- Basic SELECT
USE DATABASE sales_data
FROM customers
WHERE age > 25

-- Clustering
USE DATABASE sales_data
FROM customers
MINE CLUSTER K = 3
DISPLAY AS scatter_plot

-- Statistics
USE DATABASE sales_data
FROM customers
WHERE city = 'Mumbai'
MINE STATISTICS
```

## Project Structure

```
dqml-platform/
├── backend/
│   ├── dqml/
│   │   ├── parser/          # ANTLR4 grammar + generated parser
│   │   ├── executor/        # Query execution engine
│   │   ├── mining/          # Data mining algorithms
│   │   └── visualization/   # Chart generation
│   ├── api/                 # FastAPI REST endpoints
│   └── tests/               # Unit tests
├── frontend/
│   └── src/
│       ├── components/      # React components
│       ├── pages/           # Main pages
│       └── utils/           # Helper functions
├── data/                    # Sample datasets
└── research_gap_analysis/   # Research documentation
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Parser | ANTLR4 |
| Backend | FastAPI + Python |
| Query Execution | DuckDB / SQLite |
| Data Mining | scikit-learn |
| Visualization | Plotly |
| Frontend | React + TypeScript |

## Development Status

**Phase 1 (MVP)**: In Progress
- [x] Project structure
- [ ] DMQL parser
- [ ] Query executor
- [ ] Mining operations
- [ ] Visualization
- [ ] Web UI

## Research Foundation

Based on:
- Han, J., Fu, Y., Wang, W., et al. (1996). "DMQL: A Data Mining Query Language for Relational Databases"
- ISO/IEC 9075:2023 SQL Standard
- ISO/IEC 39075:2024 GQL - Graph Query Language

## License

MIT License
