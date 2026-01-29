"""
DQML FastAPI Backend

REST API for executing DMQL queries with data mining and visualization.

Endpoints:
- POST /api/execute - Execute a DMQL query
- GET /api/health - Health check endpoint

Usage:
    uvicorn backend.api.main:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import traceback
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dqml.parser import parse_query, DMQLQuery
from dqml.executor import SQLiteExecutor, ExecutionResult
from dqml.mining import (
    kmeans_clustering,
    dbscan_clustering,
    basic_statistics,
    correlation_analysis,
    data_profile,
    detect_anomalies
)
from dqml.visualization import (
    generate_chart,
    generate_cluster_visualization,
    generate_anomaly_visualization,
    auto_visualize,
    ChartResult
)


def convert_to_serializable(obj):
    """Convert numpy/pandas types to JSON-serializable Python types."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    else:
        return obj


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="DQML API",
    description="Data Mining Query Language - REST API for executing DMQL queries",
    version="0.1.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for query execution."""
    query: str
    data: Optional[Dict[str, List[Any]]] = None  # Optional inline data


class QueryResponse(BaseModel):
    """Response model for query execution."""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    row_count: int = 0
    mining_result: Optional[Dict[str, Any]] = None
    chart: Optional[Dict[str, Any]] = None
    sql: Optional[str] = None
    error: Optional[str] = None
    query_type: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str


# ============================================================================
# Global State
# ============================================================================

# Global executor instance
executor = SQLiteExecutor()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")


@app.post("/api/execute", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """
    Execute a DMQL query.
    
    Supports:
    - Basic SELECT queries (translated to SQL)
    - Data mining operations (CLUSTER, STATISTICS, ANOMALIES)
    - Visualization (DISPLAY AS chart_type)
    """
    try:
        query_text = request.query.strip()
        
        if not query_text:
            raise HTTPException(status_code=400, detail="Empty query")
        
        # Load inline data if provided
        if request.data:
            df = pd.DataFrame(request.data)
            # Register as 'inline_data' table
            executor.load_dataframe(df, 'inline_data')
        
        # Parse the query
        parsed = parse_query(query_text)
        
        if not parsed:
            raise HTTPException(status_code=400, detail="Failed to parse query")
        
        # Determine query type
        if parsed.mining_operation:
            return await _execute_mining_query(parsed, request)
        else:
            return await _execute_select_query(parsed, request)
            
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return QueryResponse(
            success=False,
            error=str(e)
        )


async def _execute_select_query(parsed: DMQLQuery, request: QueryRequest) -> QueryResponse:
    """Execute a basic SELECT query."""
    # Execute query using parsed DMQLQuery object
    result = executor.execute_query(parsed)
    
    # Prepare response
    if result.data is not None and not result.data.empty:
        data_records = result.data.to_dict(orient='records')
        columns = list(result.data.columns)
        row_count = len(result.data)
        
        # Check if visualization is requested
        chart_data = None
        if parsed.display_type and parsed.display_type != 'table':
            chart_result = generate_chart(
                result.data,
                parsed.display_type,
                title=f"Query Results"
            )
            chart_data = chart_result.to_dict()
        
        return QueryResponse(
            success=True,
            data=data_records,
            columns=columns,
            row_count=row_count,
            sql=result.sql_query,
            chart=chart_data,
            query_type='select'
        )
    else:
        return QueryResponse(
            success=True,
            data=[],
            columns=[],
            row_count=0,
            sql=result.sql_query,
            query_type='select'
        )


async def _execute_mining_query(parsed: DMQLQuery, request: QueryRequest) -> QueryResponse:
    """Execute a mining operation query."""
    mining_op = parsed.mining_operation
    
    # First get the data using a select query
    table_name = parsed.tables[0] if parsed.tables else 'unknown'
    select_query = f"FROM {table_name}"
    if parsed.database:
        select_query = f"USE DATABASE {parsed.database} " + select_query
    if parsed.conditions:
        select_query += f" WHERE {parsed.conditions}"
    
    # Execute the base query to get data
    result = executor.execute_query(parsed)
    
    if result.data is None or result.data.empty:
        return QueryResponse(
            success=False,
            error="No data returned from query",
            query_type='mining'
        )
    
    df = result.data
    
    # Execute mining operation
    mining_result = None
    chart_data = None
    
    if mining_op.operation_type.upper() == 'CLUSTER':
        mining_result, chart_data = await _run_clustering(df, mining_op, parsed.display_type)
    elif mining_op.operation_type.upper() == 'STATISTICS':
        mining_result, chart_data = await _run_statistics(df, mining_op, parsed.display_type)
    elif mining_op.operation_type.upper() == 'ANOMALIES':
        mining_result, chart_data = await _run_anomaly_detection(df, mining_op, parsed.display_type)
    else:
        return QueryResponse(
            success=False,
            error=f"Unknown mining operation: {mining_op.operation_type}",
            query_type='mining'
        )
    
    # Get output data
    output_data = mining_result.pop('data', df)  # Remove 'data' from mining_result
    if isinstance(output_data, pd.DataFrame):
        data_records = convert_to_serializable(output_data.to_dict(orient='records'))
        columns = list(output_data.columns)
        row_count = len(output_data)
    else:
        data_records = []
        columns = []
        row_count = 0
    
    # Convert mining_result to serializable types
    serializable_mining_result = convert_to_serializable(mining_result)
    
    return QueryResponse(
        success=True,
        data=data_records,
        columns=columns,
        row_count=row_count,
        mining_result=serializable_mining_result,
        chart=chart_data,
        sql=result.sql_query,
        query_type='mining'
    )


async def _run_clustering(
    df: pd.DataFrame,
    mining_op,
    display_as: Optional[str]
) -> tuple:
    """Run clustering operation."""
    # Get K value from parameters
    k = mining_op.parameters.get('k', 3)
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for clustering")
    
    # Run K-Means clustering
    cluster_result = kmeans_clustering(df, n_clusters=k, feature_columns=numeric_cols)
    
    # Build mining result
    mining_result = {
        'type': 'clustering',
        'method': 'kmeans',
        'n_clusters': cluster_result.n_clusters,
        'inertia': cluster_result.inertia,
        'cluster_sizes': cluster_result.cluster_sizes,
        'data': cluster_result.data
    }
    
    # Generate visualization
    chart_data = None
    if display_as:
        chart_result = generate_chart(
            cluster_result.data,
            display_as,
            x_col=numeric_cols[0],
            y_col=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0],
            color_col='cluster',
            title='Clustering Results'
        )
        chart_data = chart_result.to_dict()
    else:
        # Default to scatter plot for clustering
        chart_result = generate_cluster_visualization(
            cluster_result.data,
            feature_cols=numeric_cols[:3],
            cluster_col='cluster',
            title='K-Means Clustering'
        )
        chart_data = chart_result.to_dict()
    
    return mining_result, chart_data


async def _run_statistics(
    df: pd.DataFrame,
    mining_op,
    display_as: Optional[str]
) -> tuple:
    """Run statistics operation."""
    # Get statistics
    stats_result = basic_statistics(df)
    profile = data_profile(df)
    
    # Build mining result
    mining_result = {
        'type': 'statistics',
        'summary': stats_result.summary,
        'profile': profile,
        'data': df
    }
    
    # Generate visualization
    chart_data = None
    if display_as:
        chart_result = generate_chart(
            df, display_as,
            title='Statistics Results'
        )
        chart_data = chart_result.to_dict()
    else:
        # Default to heatmap of correlations
        chart_result = generate_chart(
            df, 'heatmap',
            title='Correlation Heatmap'
        )
        chart_data = chart_result.to_dict()
    
    return mining_result, chart_data


async def _run_anomaly_detection(
    df: pd.DataFrame,
    mining_op,
    display_as: Optional[str]
) -> tuple:
    """Run anomaly detection operation."""
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 1:
        raise ValueError("Need at least 1 numeric column for anomaly detection")
    
    # Run anomaly detection
    anomaly_result = detect_anomalies(df, method='isolation_forest', feature_columns=numeric_cols)
    
    # Get anomaly indices
    anomaly_indices = anomaly_result.data[anomaly_result.data['is_anomaly'] == True].index.tolist()
    
    # Build mining result
    mining_result = {
        'type': 'anomaly_detection',
        'method': anomaly_result.method,
        'n_anomalies': anomaly_result.n_anomalies,
        'anomaly_ratio': anomaly_result.anomaly_percentage,
        'anomaly_indices': anomaly_indices,
        'data': anomaly_result.data
    }
    
    # Generate visualization
    chart_data = None
    if display_as:
        chart_result = generate_chart(
            anomaly_result.data,
            display_as,
            title='Anomaly Detection Results'
        )
        chart_data = chart_result.to_dict()
    else:
        # Default to anomaly visualization
        chart_result = generate_anomaly_visualization(
            anomaly_result.data,
            feature_cols=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols,
            anomaly_col='is_anomaly',
            score_col='anomaly_score',
            title='Anomaly Detection'
        )
        chart_data = chart_result.to_dict()
    
    return mining_result, chart_data


# ============================================================================
# Data Management Endpoints
# ============================================================================

class LoadDataRequest(BaseModel):
    """Request to load data from CSV."""
    file_path: str
    table_name: str


class LoadDataResponse(BaseModel):
    """Response for data loading."""
    success: bool
    table_name: str
    row_count: int
    columns: List[str]
    error: Optional[str] = None


@app.post("/api/load-csv", response_model=LoadDataResponse)
async def load_csv(request: LoadDataRequest):
    """Load a CSV file into the executor."""
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")
        
        df = executor.load_csv(request.file_path, request.table_name)
        
        return LoadDataResponse(
            success=True,
            table_name=request.table_name,
            row_count=len(df),
            columns=list(df.columns)
        )
    except HTTPException:
        raise
    except Exception as e:
        return LoadDataResponse(
            success=False,
            table_name=request.table_name,
            row_count=0,
            columns=[],
            error=str(e)
        )


@app.get("/api/tables")
async def list_tables():
    """List all loaded tables."""
    return {"tables": executor.list_tables()}


# ============================================================================
# Development Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
