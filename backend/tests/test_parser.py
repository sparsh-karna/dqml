"""
Tests for DMQL Parser

These tests verify that the ANTLR4-generated parser correctly handles
various DMQL query patterns.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from backend.dqml.parser.dmql_parser import parse_query, validate_query, DMQLQuery


class TestBasicQueries:
    """Test basic query parsing."""
    
    def test_simple_select(self):
        """Test parsing a simple SELECT-like query."""
        query = """
        USE DATABASE sales_data
        FROM customers
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert 'customers' in result.tables
        assert len(result.errors) == 0
    
    def test_query_with_where(self):
        """Test parsing query with WHERE clause."""
        query = """
        USE DATABASE sales_data
        FROM customers
        WHERE age > 25
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert 'customers' in result.tables
        assert result.conditions is not None
        assert len(result.errors) == 0
    
    def test_query_with_relevance(self):
        """Test parsing query with RELEVANCE TO clause."""
        query = """
        USE DATABASE sales_data
        RELEVANCE TO name, age, city
        FROM customers
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert 'name' in result.columns
        assert 'age' in result.columns
        assert 'city' in result.columns
    
    def test_query_with_group_by(self):
        """Test parsing query with GROUP BY clause."""
        query = """
        USE DATABASE sales_data
        FROM customers
        GROUP BY city
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert 'city' in result.group_by
    
    def test_query_with_order_by(self):
        """Test parsing query with ORDER BY clause."""
        query = """
        USE DATABASE sales_data
        FROM customers
        ORDER BY age DESC
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert ('age', 'DESC') in result.order_by


class TestMiningQueries:
    """Test mining operation parsing."""
    
    def test_clustering_query(self):
        """Test parsing K-Means clustering query."""
        query = """
        USE DATABASE sales_data
        FROM customers
        MINE CLUSTER K = 5
        """
        
        result = parse_query(query)
        
        assert result.mining_operation is not None
        assert result.mining_operation.operation_type == 'CLUSTER'
        assert result.mining_operation.parameters.get('k') == 5
    
    def test_statistics_query(self):
        """Test parsing statistics query."""
        query = """
        USE DATABASE sales_data
        FROM customers
        MINE STATISTICS
        """
        
        result = parse_query(query)
        
        assert result.mining_operation is not None
        assert result.mining_operation.operation_type == 'STATISTICS'
    
    def test_anomaly_detection_query(self):
        """Test parsing anomaly detection query."""
        query = """
        USE DATABASE sales_data
        FROM customers
        MINE ANOMALIES
        """
        
        result = parse_query(query)
        
        assert result.mining_operation is not None
        assert result.mining_operation.operation_type == 'ANOMALIES'
    
    def test_association_rules_query(self):
        """Test parsing association rules query."""
        query = """
        USE DATABASE transactions
        FROM purchases
        MINE ASSOCIATION_RULES
        """
        
        result = parse_query(query)
        
        assert result.mining_operation is not None
        assert result.mining_operation.operation_type == 'ASSOCIATION_RULES'


class TestDisplayQueries:
    """Test display/visualization type parsing."""
    
    def test_scatter_plot(self):
        """Test parsing query with scatter plot display."""
        query = """
        USE DATABASE sales_data
        FROM customers
        MINE CLUSTER K = 3
        DISPLAY AS scatter_plot
        """
        
        result = parse_query(query)
        
        assert result.display_type == 'scatter_plot'
    
    def test_bar_chart(self):
        """Test parsing query with bar chart display."""
        query = """
        USE DATABASE sales_data
        FROM customers
        DISPLAY AS bar_chart
        """
        
        result = parse_query(query)
        
        assert result.display_type == 'bar_chart'
    
    def test_heatmap(self):
        """Test parsing query with heatmap display."""
        query = """
        USE DATABASE sales_data
        FROM customers
        DISPLAY AS heatmap
        """
        
        result = parse_query(query)
        
        assert result.display_type == 'heatmap'


class TestInterestMeasures:
    """Test WITH clause and interest measures parsing."""
    
    def test_confidence_measure(self):
        """Test parsing query with confidence measure."""
        query = """
        USE DATABASE sales_data
        FROM transactions
        MINE ASSOCIATION_RULES
        WITH confidence = 0.8
        """
        
        result = parse_query(query)
        
        assert result.interest_measures is not None
        assert result.interest_measures.confidence == 0.8
    
    def test_multiple_measures(self):
        """Test parsing query with multiple interest measures."""
        query = """
        USE DATABASE sales_data
        FROM transactions
        MINE ASSOCIATION_RULES
        WITH support = 0.1, confidence = 0.7
        """
        
        result = parse_query(query)
        
        assert result.interest_measures is not None
        assert result.interest_measures.support == 0.1
        assert result.interest_measures.confidence == 0.7


class TestComplexQueries:
    """Test complex query patterns."""
    
    def test_full_query(self):
        """Test parsing a complete DMQL query with all clauses."""
        query = """
        USE DATABASE climate_data
        RELEVANCE TO temperature, humidity, pressure
        FROM weather_stations
        WHERE temperature > 30
        GROUP BY city
        ORDER BY temperature DESC
        MINE ANOMALIES
        WITH confidence_level = 0.95
        DISPLAY AS heatmap
        """
        
        result = parse_query(query)
        
        assert result.database == 'climate_data'
        assert 'temperature' in result.columns
        assert 'weather_stations' in result.tables
        assert result.conditions is not None
        assert 'city' in result.group_by
        assert len(result.order_by) > 0
        assert result.mining_operation.operation_type == 'ANOMALIES'
        assert result.interest_measures.confidence_level == 0.95
        assert result.display_type == 'heatmap'
    
    def test_multiple_tables(self):
        """Test parsing query with multiple tables."""
        query = """
        USE DATABASE sales_data
        FROM customers, orders, products
        """
        
        result = parse_query(query)
        
        assert len(result.tables) == 3
        assert 'customers' in result.tables
        assert 'orders' in result.tables
        assert 'products' in result.tables


class TestQueryValidation:
    """Test query validation functionality."""
    
    def test_valid_query(self):
        """Test validation of a valid query."""
        query = """
        USE DATABASE sales_data
        FROM customers
        """
        
        is_valid, errors = validate_query(query)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_case_insensitivity(self):
        """Test that keywords are case-insensitive."""
        query = """
        use database sales_data
        from customers
        where age > 25
        """
        
        is_valid, errors = validate_query(query)
        
        assert is_valid
        assert len(errors) == 0


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_string_values_single_quotes(self):
        """Test parsing string values with single quotes."""
        query = """
        USE DATABASE sales_data
        FROM customers
        WHERE city = 'Mumbai'
        """
        
        result = parse_query(query)
        
        assert result.conditions is not None
        assert len(result.errors) == 0
    
    def test_string_values_double_quotes(self):
        """Test parsing string values with double quotes."""
        query = """
        USE DATABASE sales_data
        FROM customers
        WHERE city = "Delhi"
        """
        
        result = parse_query(query)
        
        assert result.conditions is not None
        assert len(result.errors) == 0
    
    def test_numeric_comparison(self):
        """Test parsing numeric comparisons."""
        query = """
        USE DATABASE sales_data
        FROM customers
        WHERE purchase_amount >= 5000.50
        """
        
        result = parse_query(query)
        
        assert result.conditions is not None
        assert len(result.errors) == 0
    
    def test_comments_line(self):
        """Test that line comments are ignored."""
        query = """
        -- This is a comment
        USE DATABASE sales_data
        FROM customers
        -- Another comment
        """
        
        result = parse_query(query)
        
        assert result.database == 'sales_data'
        assert len(result.errors) == 0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run basic tests manually
    print("=" * 60)
    print("DMQL Parser Tests")
    print("=" * 60)
    
    # Test 1: Basic query
    print("\nTest 1: Basic query parsing")
    query1 = """
    USE DATABASE sales_data
    FROM customers
    WHERE age > 25
    """
    result1 = parse_query(query1)
    print(f"  Database: {result1.database}")
    print(f"  Tables: {result1.tables}")
    print(f"  Conditions: {result1.conditions}")
    print(f"  Errors: {result1.errors}")
    assert result1.database == 'sales_data', "Database should be 'sales_data'"
    print("  ✓ Basic query parsed successfully")
    
    # Test 2: Mining query
    print("\nTest 2: Mining query parsing")
    query2 = """
    USE DATABASE sales_data
    FROM customers
    MINE CLUSTER K = 5
    DISPLAY AS scatter_plot
    """
    result2 = parse_query(query2)
    print(f"  Mining operation: {result2.mining_operation}")
    print(f"  Display type: {result2.display_type}")
    print(f"  Errors: {result2.errors}")
    assert result2.mining_operation is not None, "Should have mining operation"
    assert result2.mining_operation.operation_type == 'CLUSTER', "Should be CLUSTER"
    print("  ✓ Mining query parsed successfully")
    
    # Test 3: Complex query
    print("\nTest 3: Complex query parsing")
    query3 = """
    USE DATABASE climate_india
    RELEVANCE TO temperature, humidity, air_quality
    FROM weather_stations
    WHERE temperature > 30
    GROUP BY city
    MINE STATISTICS
    WITH confidence = 0.95
    DISPLAY AS heatmap
    """
    result3 = parse_query(query3)
    print(f"  Database: {result3.database}")
    print(f"  Columns: {result3.columns}")
    print(f"  Tables: {result3.tables}")
    print(f"  Group by: {result3.group_by}")
    print(f"  Mining: {result3.mining_operation}")
    print(f"  Display: {result3.display_type}")
    print(f"  Errors: {result3.errors}")
    print("  ✓ Complex query parsed successfully")
    
    # Test 4: Validation
    print("\nTest 4: Query validation")
    is_valid, errors = validate_query(query1)
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {errors}")
    assert is_valid, "Query should be valid"
    print("  ✓ Query validation passed")
    
    print("\n" + "=" * 60)
    print("All manual tests passed!")
    print("=" * 60)
    print("\nTo run full pytest suite: pytest backend/tests/test_parser.py -v")
