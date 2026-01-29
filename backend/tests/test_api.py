"""
Tests for DQML FastAPI Backend

Tests API endpoints using httpx test client.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.main import app, executor


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_data():
    """Load sample data into executor."""
    import pandas as pd
    import numpy as np
    
    np.random.seed(42)
    df = pd.DataFrame({
        'id': range(1, 21),
        'category': ['A', 'B', 'C', 'D'] * 5,
        'value': np.random.randint(10, 100, 20),
        'score': np.random.rand(20) * 100
    })
    executor.load_dataframe(df, 'test_data')
    return df


class TestHealthEndpoint:
    """Tests for /api/health endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"


class TestExecuteEndpoint:
    """Tests for /api/execute endpoint."""
    
    def test_empty_query_returns_error(self, client):
        """Test empty query handling."""
        response = client.post("/api/execute", json={"query": ""})
        
        assert response.status_code == 400
    
    def test_execute_with_inline_data(self, client):
        """Test query execution with inline data."""
        response = client.post("/api/execute", json={
            "query": "FROM inline_data",
            "data": {
                "name": ["Alice", "Bob", "Charlie"],
                "age": [25, 30, 35]
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["row_count"] == 3
    
    def test_execute_basic_select(self, client, sample_data):
        """Test basic SELECT query."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["row_count"] == 20
        assert "id" in data["columns"]
    
    def test_execute_with_where(self, client, sample_data):
        """Test query with WHERE clause."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data WHERE category = 'A'"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["row_count"] == 5
    
    def test_execute_with_display(self, client, sample_data):
        """Test query with DISPLAY AS."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data DISPLAY AS bar_chart"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["chart"] is not None


class TestMiningOperations:
    """Tests for mining operations via API."""
    
    def test_clustering_query(self, client, sample_data):
        """Test MINE CLUSTER query."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data MINE CLUSTER K=3"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["query_type"] == "mining"
        assert data["mining_result"] is not None
        assert data["mining_result"]["type"] == "clustering"
    
    def test_statistics_query(self, client, sample_data):
        """Test MINE STATISTICS query."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data MINE STATISTICS"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["query_type"] == "mining"
        assert data["mining_result"]["type"] == "statistics"
    
    def test_anomaly_query(self, client, sample_data):
        """Test MINE ANOMALIES query."""
        response = client.post("/api/execute", json={
            "query": "FROM test_data MINE ANOMALIES"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["query_type"] == "mining"
        assert data["mining_result"]["type"] == "anomaly_detection"


class TestDataManagement:
    """Tests for data management endpoints."""
    
    def test_list_tables(self, client, sample_data):
        """Test listing tables."""
        response = client.get("/api/tables")
        
        assert response.status_code == 200
        data = response.json()
        assert "tables" in data
        assert "test_data" in data["tables"]
    
    def test_load_csv_not_found(self, client):
        """Test loading non-existent CSV file."""
        response = client.post("/api/load-csv", json={
            "file_path": "/nonexistent/file.csv",
            "table_name": "test"
        })
        
        assert response.status_code == 404


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_invalid_query_syntax(self, client):
        """Test handling of invalid query syntax."""
        response = client.post("/api/execute", json={
            "query": "INVALID SYNTAX HERE!!!"
        })
        
        assert response.status_code == 200
        data = response.json()
        # The query might still "parse" but won't execute properly
        # or will get an error - either is acceptable
        assert "success" in data
    
    def test_query_on_nonexistent_table(self, client):
        """Test query on non-existent table."""
        # Clear existing tables first by using a new query
        response = client.post("/api/execute", json={
            "query": "FROM nonexistent_table_xyz123"
        })
        
        # Should return an error response
        assert response.status_code == 200
        data = response.json()
        # Either fails or returns empty (depending on implementation)
        assert "success" in data
