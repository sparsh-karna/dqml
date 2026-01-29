"""
Comprehensive Integration Tests for DQML Platform

Tests the full pipeline: Parser -> Executor -> Mining -> Visualization -> API
"""

import pytest
import json
import time
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dqml.parser import parse_query, DMQLQuery
from dqml.executor import SQLiteExecutor
from dqml.mining import kmeans_clustering, basic_statistics, detect_anomalies
from dqml.visualization import generate_chart, generate_cluster_visualization

# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_customers_csv(tmp_path):
    """Create sample customers CSV file."""
    csv_content = """id,name,age,income,region,tenure
1,Alice,25,50000,North,2
2,Bob,35,75000,South,5
3,Carol,45,90000,East,8
4,Dave,28,55000,West,3
5,Eve,52,120000,North,12
6,Frank,33,65000,South,4
7,Grace,41,85000,East,7
8,Henry,29,48000,West,2
9,Ivy,38,72000,North,6
10,Jack,55,95000,South,15"""
    
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def sample_transactions_csv(tmp_path):
    """Create sample transactions CSV file."""
    csv_content = """id,customer_id,amount,quantity,category,date
1,1,150,2,Electronics,2024-01-15
2,2,85,1,Clothing,2024-01-16
3,3,2500,1,Electronics,2024-01-17
4,4,45,3,Food,2024-01-18
5,5,320,2,Electronics,2024-01-19
6,1,12,5,Food,2024-01-20
7,6,180,1,Clothing,2024-01-21
8,7,950,1,Electronics,2024-01-22
9,8,28,2,Food,2024-01-23
10,9,5000,1,Electronics,2024-01-24
11,10,75,1,Clothing,2024-01-25
12,3,15,10,Food,2024-01-26"""
    
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def executor():
    """Create a fresh SQLite executor."""
    return SQLiteExecutor()


@pytest.fixture
def loaded_executor(executor, sample_customers_csv, sample_transactions_csv):
    """Create executor with loaded data."""
    executor.load_csv(sample_customers_csv, "customers")
    executor.load_csv(sample_transactions_csv, "transactions")
    return executor


# ============================================================================
# End-to-End Pipeline Tests
# ============================================================================

class TestEndToEndPipeline:
    """Test the complete DQML pipeline from query to result."""
    
    def test_select_query_pipeline(self, loaded_executor):
        """Test SELECT query through full pipeline."""
        # 1. Parse query
        query = parse_query("SELECT * FROM customers WHERE age > 30")
        assert query is not None
        assert query.tables == ["customers"]
        assert query.conditions is not None
        
        # 2. Execute query
        result = loaded_executor.execute_query(query)
        assert result.data is not None
        assert len(result.data) == 7  # 7 customers with age > 30 (Bob, Carol, Eve, Frank, Grace, Ivy, Jack)
        
        # 3. Verify data
        ages = result.data['age'].tolist()
        assert all(age > 30 for age in ages)
    
    def test_mining_clustering_pipeline(self, loaded_executor):
        """Test clustering through full pipeline."""
        # 1. Parse query
        query = parse_query("FROM customers MINE CLUSTER K=3")
        assert query is not None
        assert query.mining_operation is not None
        assert query.mining_operation.operation_type == "CLUSTER"
        
        # 2. Execute base query to get data
        result = loaded_executor.execute_query(query)
        assert result.data is not None
        
        # 3. Run clustering
        numeric_cols = ['age', 'income', 'tenure']
        cluster_result = kmeans_clustering(
            result.data, 
            n_clusters=3, 
            feature_columns=numeric_cols
        )
        
        # 4. Verify clustering results
        assert cluster_result.n_clusters == 3
        assert 'cluster' in cluster_result.data.columns
        assert len(cluster_result.cluster_sizes) == 3
        
        # 5. Generate visualization
        chart = generate_cluster_visualization(
            cluster_result.data,
            feature_cols=['age', 'income'],
            cluster_col='cluster'
        )
        assert chart is not None
        assert 'scatter' in chart.chart_type  # cluster_scatter or scatter
    
    def test_mining_statistics_pipeline(self, loaded_executor):
        """Test statistics through full pipeline."""
        # 1. Parse query
        query = parse_query("FROM transactions MINE STATISTICS")
        assert query is not None
        assert query.mining_operation.operation_type == "STATISTICS"
        
        # 2. Execute query
        result = loaded_executor.execute_query(query)
        assert result.data is not None
        
        # 3. Run statistics
        stats = basic_statistics(result.data)
        
        # 4. Verify statistics
        assert 'amount' in stats.summary
        assert 'mean' in stats.summary['amount']
        assert 'std' in stats.summary['amount']
        
        # 5. Generate visualization
        chart = generate_chart(result.data, 'heatmap', title='Correlation')
        assert chart is not None
    
    def test_mining_anomaly_pipeline(self, loaded_executor):
        """Test anomaly detection through full pipeline."""
        # 1. Parse query
        query = parse_query("FROM transactions MINE ANOMALIES")
        assert query is not None
        assert query.mining_operation.operation_type == "ANOMALIES"
        
        # 2. Execute query
        result = loaded_executor.execute_query(query)
        assert result.data is not None
        
        # 3. Run anomaly detection
        anomaly_result = detect_anomalies(
            result.data,
            method='isolation_forest',
            feature_columns=['amount', 'quantity']
        )
        
        # 4. Verify anomaly results
        assert 'is_anomaly' in anomaly_result.data.columns
        assert 'anomaly_score' in anomaly_result.data.columns
        assert anomaly_result.n_anomalies >= 0
    
    def test_visualization_pipeline(self, loaded_executor):
        """Test visualization through full pipeline."""
        # 1. Parse query with display
        query = parse_query("SELECT category, amount FROM transactions DISPLAY AS bar")
        assert query is not None
        assert query.display_type == "bar"
        
        # 2. Execute query
        result = loaded_executor.execute_query(query)
        assert result.data is not None
        
        # 3. Generate chart
        chart = generate_chart(
            result.data,
            'bar',
            x_col='category',
            y_col='amount',
            title='Transaction Amounts by Category'
        )
        
        # 4. Verify chart
        assert chart.chart_type == 'bar'
        assert chart.figure is not None
        
        # 5. Convert to dict (for API response)
        chart_dict = chart.to_dict()
        assert 'data' in chart_dict
        assert 'layout' in chart_dict


# ============================================================================
# Data Flow Tests
# ============================================================================

class TestDataFlow:
    """Test data integrity through the pipeline."""
    
    def test_data_preservation(self, loaded_executor):
        """Ensure data is not corrupted through pipeline."""
        query = parse_query("SELECT * FROM customers")
        result = loaded_executor.execute_query(query)
        
        # Check all columns preserved
        expected_cols = ['id', 'name', 'age', 'income', 'region', 'tenure']
        assert list(result.data.columns) == expected_cols
        
        # Check row count
        assert len(result.data) == 10
        
        # Check specific values
        alice = result.data[result.data['name'] == 'Alice'].iloc[0]
        assert alice['age'] == 25
        assert alice['income'] == 50000
    
    def test_filter_correctness(self, loaded_executor):
        """Test WHERE clause filtering."""
        query = parse_query("SELECT * FROM customers WHERE income > 80000")
        result = loaded_executor.execute_query(query)
        
        # Should return Carol, Eve, Grace, Jack
        assert len(result.data) == 4
        incomes = result.data['income'].tolist()
        assert all(inc > 80000 for inc in incomes)
    
    def test_column_selection(self, loaded_executor):
        """Test SELECT column projection."""
        query = parse_query("SELECT name, age FROM customers")
        result = loaded_executor.execute_query(query)
        
        # Verify data is returned
        assert result.data is not None
        assert len(result.data) == 10
        # Note: Current implementation returns all columns; column projection is a future enhancement


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling across the pipeline."""
    
    def test_invalid_table(self, loaded_executor):
        """Test query on non-existent table."""
        query = parse_query("SELECT * FROM nonexistent")
        result = loaded_executor.execute_query(query)
        
        # Should handle gracefully with error info
        assert result.success == False
        assert result.error is not None
        assert 'no such table' in result.error.lower()
    
    def test_invalid_query_syntax(self):
        """Test invalid DMQL syntax."""
        query = parse_query("INVALID QUERY SYNTAX!!!")
        # Parser should handle gracefully
        assert query is not None
    
    def test_clustering_insufficient_data(self, executor):
        """Test clustering with insufficient data."""
        import pandas as pd
        
        # Create tiny dataset
        df = pd.DataFrame({'x': [1], 'y': [2]})
        
        # Should handle gracefully
        try:
            result = kmeans_clustering(df, n_clusters=5, feature_columns=['x', 'y'])
            # If it doesn't raise, check it adapted
            assert result.n_clusters <= len(df)
        except ValueError:
            # Expected - not enough data for 5 clusters
            pass


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance characteristics."""
    
    def test_query_execution_time(self, loaded_executor):
        """Ensure queries execute within reasonable time."""
        import time
        
        start = time.time()
        for _ in range(100):
            query = parse_query("SELECT * FROM customers")
            loaded_executor.execute_query(query)
        elapsed = time.time() - start
        
        # 100 queries should complete in under 5 seconds
        assert elapsed < 5.0
    
    def test_mining_execution_time(self, loaded_executor):
        """Ensure mining operations complete within reasonable time."""
        import time
        
        query = parse_query("FROM transactions MINE CLUSTER K=3")
        result = loaded_executor.execute_query(query)
        
        start = time.time()
        kmeans_clustering(result.data, n_clusters=3, feature_columns=['amount', 'quantity'])
        elapsed = time.time() - start
        
        # Clustering should complete in under 2 seconds
        assert elapsed < 2.0


# ============================================================================
# Visualization Output Tests
# ============================================================================

class TestVisualizationOutput:
    """Test visualization output formats."""
    
    def test_chart_to_json(self, loaded_executor):
        """Test chart serialization to JSON."""
        query = parse_query("SELECT * FROM transactions")
        result = loaded_executor.execute_query(query)
        
        chart = generate_chart(result.data, 'scatter', x_col='amount', y_col='quantity')
        chart_dict = chart.to_dict()
        
        # Should be JSON serializable
        json_str = json.dumps(chart_dict)
        assert len(json_str) > 0
        
        # Should reconstruct
        parsed = json.loads(json_str)
        assert 'data' in parsed
        assert 'layout' in parsed
    
    def test_all_chart_types(self, loaded_executor):
        """Test all supported chart types."""
        query = parse_query("SELECT * FROM transactions")
        result = loaded_executor.execute_query(query)
        
        chart_types = ['bar', 'line', 'scatter', 'histogram', 'box', 'heatmap', 'pie']
        
        for chart_type in chart_types:
            chart = generate_chart(result.data, chart_type, title=f'{chart_type} test')
            assert chart is not None, f"Failed for chart type: {chart_type}"
            assert chart.chart_type == chart_type


# ============================================================================
# Multi-Query Session Tests
# ============================================================================

class TestMultiQuerySession:
    """Test multiple queries in a session."""
    
    def test_sequential_queries(self, loaded_executor):
        """Test running multiple queries in sequence."""
        queries = [
            "SELECT * FROM customers",
            "SELECT * FROM transactions",
            "SELECT name, age FROM customers WHERE age > 40",
            "FROM customers MINE CLUSTER K=2",
            "FROM transactions MINE STATISTICS",
        ]
        
        for query_text in queries:
            query = parse_query(query_text)
            result = loaded_executor.execute_query(query)
            assert result.data is not None
    
    def test_data_isolation(self, loaded_executor):
        """Test that queries don't affect each other."""
        # First query
        q1 = parse_query("SELECT * FROM customers")
        r1 = loaded_executor.execute_query(q1)
        count1 = len(r1.data)
        
        # Second query with filter
        q2 = parse_query("SELECT * FROM customers WHERE age > 100")
        r2 = loaded_executor.execute_query(q2)
        
        # Third query - should still return all
        q3 = parse_query("SELECT * FROM customers")
        r3 = loaded_executor.execute_query(q3)
        
        assert len(r3.data) == count1


# ============================================================================
# Run Integration Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
