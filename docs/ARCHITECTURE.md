# DQML Architecture

## System Overview

DQML is a full-stack data mining query platform consisting of three main layers:

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│              (Monaco Editor + Plotly)                    │
├─────────────────────────────────────────────────────────┤
│                    FastAPI Backend                       │
│                   (REST API Layer)                       │
├─────────────────────────────────────────────────────────┤
│                    DQML Core Engine                      │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  ┌─────────────┐ │
│  │ Parser  │→ │ Executor │→ │ Mining │→ │Visualization│ │
│  │(ANTLR4) │  │ (SQLite) │  │(sklearn)│  │  (Plotly)   │ │
│  └─────────┘  └──────────┘  └────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Parser (ANTLR4)

**Location:** `backend/dqml/parser/`

The parser uses ANTLR4 to convert DMQL query strings into structured Python objects.

```
DMQL Query String
       ↓
  ANTLR4 Lexer
       ↓
  ANTLR4 Parser
       ↓
  Parse Tree
       ↓
  DMQLQueryVisitor
       ↓
  DMQLQuery Object
```

**Key Files:**
- `DMQL.g4` - ANTLR4 grammar definition
- `DMQLLexer.py` - Generated lexer
- `DMQLParser.py` - Generated parser
- `dmql_parser.py` - High-level Python interface

**DMQLQuery Object:**
```python
@dataclass
class DMQLQuery:
    raw_query: str
    database: Optional[str]
    tables: List[str]
    columns: List[str]
    conditions: Optional[Condition]
    mining_operation: Optional[MiningOperation]
    display_type: Optional[str]
```

### 2. Executor (SQLite)

**Location:** `backend/dqml/executor/`

The executor translates parsed DMQL queries to SQL and executes them against SQLite.

```
DMQLQuery Object
       ↓
  SQL Generator
       ↓
  SQLite Engine
       ↓
  ExecutionResult
```

**Key Features:**
- In-memory SQLite database
- CSV file loading via pandas
- Automatic type inference
- Query result caching

**ExecutionResult Object:**
```python
@dataclass
class ExecutionResult:
    success: bool
    data: Optional[pd.DataFrame]
    sql_query: str
    row_count: int
    error: Optional[str]
    metadata: Dict[str, Any]
```

### 3. Mining Operations

**Location:** `backend/dqml/mining/`

Data mining algorithms implemented using scikit-learn.

#### Clustering (`clustering.py`)

```
DataFrame
    ↓
Feature Selection (numeric columns)
    ↓
StandardScaler (normalization)
    ↓
KMeans / DBSCAN
    ↓
ClusteringResult
```

**Algorithms:**
- K-Means clustering (default)
- DBSCAN (density-based)

#### Statistics (`statistics.py`)

```
DataFrame
    ↓
Descriptive Statistics (pandas describe)
    ↓
Correlation Analysis (pearson, spearman)
    ↓
Data Profiling
    ↓
StatisticsResult
```

#### Anomaly Detection (`anomaly_detection.py`)

```
DataFrame
    ↓
Feature Selection
    ↓
Isolation Forest / Z-Score / IQR
    ↓
AnomalyResult
```

**Algorithms:**
- Isolation Forest (default)
- Z-Score method
- IQR method

### 4. Visualization (Plotly)

**Location:** `backend/dqml/visualization/`

Generates interactive Plotly charts from query results.

```
DataFrame + Chart Type
         ↓
    Chart Factory
         ↓
    Plotly Figure
         ↓
    JSON (for API)
```

**Supported Charts:**
- Bar, Line, Scatter
- Histogram, Box plot
- Heatmap (correlation)
- Pie chart
- Data table

### 5. API Layer (FastAPI)

**Location:** `backend/api/`

RESTful API that orchestrates all components.

```
HTTP Request
      ↓
FastAPI Router
      ↓
Request Validation (Pydantic)
      ↓
Query Execution Pipeline:
  1. Parse query
  2. Execute against SQLite
  3. Run mining operation (if any)
  4. Generate visualization (if any)
      ↓
JSON Response
```

### 6. Frontend (React)

**Location:** `frontend/`

Single-page application for query editing and result visualization.

```
┌────────────────────────────────────────────┐
│              DQML Query Editor             │
│  ┌──────────────────────────────────────┐  │
│  │         Monaco Editor               │  │
│  │  FROM customers MINE CLUSTER K=3    │  │
│  └──────────────────────────────────────┘  │
│         [Execute Query]                    │
├────────────────────────────────────────────┤
│              Results Panel                 │
│  ┌──────────────┐  ┌───────────────────┐  │
│  │ Data Table   │  │   Plotly Chart    │  │
│  │ id | name    │  │       📊          │  │
│  │ 1  | Alice   │  │    (scatter)      │  │
│  └──────────────┘  └───────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │         Mining Results               │  │
│  │  Clusters: 3, Sizes: [4, 3, 3]      │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

---

## Data Flow

### Query Execution Flow

```
1. User enters DMQL query in Monaco Editor
                    ↓
2. Frontend POSTs to /api/execute
                    ↓
3. FastAPI receives request, validates with Pydantic
                    ↓
4. Parser converts query string to DMQLQuery object
                    ↓
5. Executor generates SQL and queries SQLite
                    ↓
6. If MINE clause present:
   - Run appropriate mining algorithm
   - Add results to DataFrame (e.g., cluster column)
                    ↓
7. If DISPLAY AS clause present:
   - Generate Plotly chart
   - Convert to JSON
                    ↓
8. Return QueryResponse with data, mining_result, chart
                    ↓
9. Frontend renders:
   - Data in table
   - Chart via react-plotly.js
   - Mining statistics
```

---

## Directory Structure

```
dqml/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py           # FastAPI application
│   ├── dqml/
│   │   ├── __init__.py
│   │   ├── parser/
│   │   │   ├── __init__.py
│   │   │   ├── DMQL.g4       # ANTLR4 grammar
│   │   │   ├── DMQLLexer.py  # Generated
│   │   │   ├── DMQLParser.py # Generated
│   │   │   └── dmql_parser.py
│   │   ├── executor/
│   │   │   ├── __init__.py
│   │   │   └── sqlite_executor.py
│   │   ├── mining/
│   │   │   ├── __init__.py
│   │   │   ├── clustering.py
│   │   │   ├── statistics.py
│   │   │   └── anomaly_detection.py
│   │   └── visualization/
│   │       ├── __init__.py
│   │       └── charts.py
│   └── tests/
│       ├── test_parser.py
│       ├── test_mining.py
│       ├── test_visualization.py
│       ├── test_api.py
│       └── test_integration.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   ├── API.md
│   ├── LANGUAGE_GUIDE.md
│   └── ARCHITECTURE.md
├── requirements.txt
└── README.md
```

---

## Technology Decisions

### Why ANTLR4?

- Industry-standard parser generator
- Generates clean visitor pattern code
- Easy grammar modifications
- Well-documented

### Why SQLite?

- Zero configuration
- In-memory option for fast queries
- Portable (single file)
- Good pandas integration

### Why scikit-learn?

- Industry standard for ML
- Well-tested algorithms
- Consistent API
- Good documentation

### Why Plotly?

- Interactive charts
- JSON serializable
- React integration available
- Wide chart variety

### Why FastAPI?

- Automatic OpenAPI docs
- Pydantic validation
- Async support
- High performance

### Why React + Vite?

- Fast development experience
- TypeScript support
- Monaco Editor integration
- Hot module replacement

---

## Scalability Considerations

### Current Limitations

1. **In-memory SQLite**: Limited by available RAM
2. **Single-threaded**: No parallel query execution
3. **No persistence**: Data lost on restart
4. **No authentication**: Not production-ready

### Future Improvements

1. **Database**: Switch to PostgreSQL/DuckDB for larger datasets
2. **Caching**: Add Redis for query result caching
3. **Workers**: Use Celery for async mining operations
4. **Auth**: Implement JWT authentication
5. **Persistence**: Add file-based or cloud storage

---

## Extension Points

### Adding New Mining Operations

1. Create new module in `backend/dqml/mining/`
2. Define result dataclass
3. Add to `__init__.py` exports
4. Update API to handle new operation
5. Add grammar rule in `DMQL.g4`
6. Regenerate parser

### Adding New Chart Types

1. Add function in `charts.py`
2. Register in chart factory
3. Update grammar if new keyword needed
4. Add frontend rendering support
