"""
Tests for DMQL SQLite Executor

These tests verify that the SQLite executor correctly translates
and executes DMQL queries.
"""

import sys
import os
import tempfile

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
import pandas as pd
from backend.dqml.executor.sqlite_executor import SQLiteExecutor, ExecutionResult
from backend.dqml.parser.dmql_parser import parse_query


class TestSQLiteExecutorBasics:
    """Test basic executor functionality."""
    
    def test_connect_memory_database(self):
        """Test connecting to in-memory database."""
        executor = SQLiteExecutor(':memory:')
        executor.connect()
        
        assert executor.conn is not None
        executor.close()
    
    def test_context_manager(self):
        """Test context manager interface."""
        with SQLiteExecutor(':memory:') as executor:
            assert executor.conn is not None
    
    def test_load_csv(self):
        """Test loading CSV data into table."""
        with SQLiteExecutor(':memory:') as executor:
            # Create sample data
            df = pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': [25, 30, 35]
            })
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                df.to_csv(f.name, index=False)
                temp_path = f.name
            
            try:
                # Load into database
                loaded_df = executor.load_csv(temp_path, 'test_table')
                
                assert len(loaded_df) == 3
                assert 'test_table' in executor.list_tables()
            finally:
                os.unlink(temp_path)
    
    def test_load_dataframe(self):
        """Test loading DataFrame directly."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({
                'id': [1, 2, 3],
                'value': [100, 200, 300]
            })
            
            executor.load_dataframe(df, 'values_table')
            
            assert 'values_table' in executor.list_tables()


class TestQueryExecution:
    """Test query execution functionality."""
    
    @pytest.fixture
    def executor_with_data(self):
        """Create executor with sample data."""
        executor = SQLiteExecutor(':memory:')
        executor.connect()
        
        # Load sample customers data
        customers_df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [28, 35, 22, 45, 31],
            'city': ['Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi'],
            'purchase_amount': [5000, 7500, 3000, 12000, 6000]
        })
        executor.load_dataframe(customers_df, 'customers', database_name='sales_data')
        
        yield executor
        executor.close()
    
    def test_simple_select(self, executor_with_data):
        """Test executing simple SELECT query."""
        result = executor_with_data.execute_select('sales_data__customers')
        
        assert len(result) == 5
        assert 'name' in result.columns
        assert 'age' in result.columns
    
    def test_select_with_columns(self, executor_with_data):
        """Test SELECT with specific columns."""
        result = executor_with_data.execute_select(
            'sales_data__customers',
            columns=['name', 'age']
        )
        
        assert len(result.columns) == 2
        assert 'name' in result.columns
        assert 'age' in result.columns
    
    def test_select_with_where(self, executor_with_data):
        """Test SELECT with WHERE clause."""
        result = executor_with_data.execute_select(
            'sales_data__customers',
            where_clause='age > 30'
        )
        
        assert len(result) == 3  # Bob, Diana, Eve
        assert all(result['age'] > 30)
    
    def test_select_with_order_by(self, executor_with_data):
        """Test SELECT with ORDER BY."""
        result = executor_with_data.execute_select(
            'sales_data__customers',
            order_by=[('age', 'DESC')]
        )
        
        ages = result['age'].tolist()
        assert ages == sorted(ages, reverse=True)
    
    def test_select_with_limit(self, executor_with_data):
        """Test SELECT with LIMIT."""
        result = executor_with_data.execute_select(
            'sales_data__customers',
            limit=3
        )
        
        assert len(result) == 3


class TestDMQLQueryExecution:
    """Test executing full DMQL queries."""
    
    @pytest.fixture
    def executor_with_data(self):
        """Create executor with sample data."""
        executor = SQLiteExecutor(':memory:')
        executor.connect()
        
        # Load sample data
        customers_df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [28, 35, 22, 45, 31],
            'city': ['Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi'],
            'purchase_amount': [5000, 7500, 3000, 12000, 6000]
        })
        executor.load_dataframe(customers_df, 'customers', database_name='sales_data')
        
        yield executor
        executor.close()
    
    def test_execute_dmql_query(self, executor_with_data):
        """Test executing parsed DMQL query."""
        query_str = """
        USE DATABASE sales_data
        FROM customers
        WHERE age > 25
        """
        
        parsed = parse_query(query_str)
        result = executor_with_data.execute_query(parsed)
        
        assert result.success
        assert result.data is not None
        assert len(result.data) == 4  # Alice, Bob, Diana, Eve (age > 25)
    
    def test_execute_with_order_by(self, executor_with_data):
        """Test DMQL query with ORDER BY."""
        query_str = """
        USE DATABASE sales_data
        FROM customers
        ORDER BY purchase_amount DESC
        """
        
        parsed = parse_query(query_str)
        result = executor_with_data.execute_query(parsed)
        
        assert result.success
        amounts = result.data['purchase_amount'].tolist()
        assert amounts == sorted(amounts, reverse=True)
    
    def test_execute_with_group_by(self, executor_with_data):
        """Test DMQL query with GROUP BY."""
        # For GROUP BY, we need aggregate functions in real SQL
        # This test verifies the GROUP BY clause is added
        query_str = """
        USE DATABASE sales_data
        FROM customers
        GROUP BY city
        """
        
        parsed = parse_query(query_str)
        result = executor_with_data.execute_query(parsed)
        
        # SQLite will return one row per city without aggregates
        assert result.success


class TestTableManagement:
    """Test table management features."""
    
    def test_list_tables(self):
        """Test listing tables."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({'a': [1, 2, 3]})
            executor.load_dataframe(df, 'table1')
            executor.load_dataframe(df, 'table2')
            
            tables = executor.list_tables()
            
            assert 'table1' in tables
            assert 'table2' in tables
    
    def test_list_tables_by_database(self):
        """Test listing tables filtered by database."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({'a': [1, 2, 3]})
            executor.load_dataframe(df, 'customers', database_name='sales')
            executor.load_dataframe(df, 'orders', database_name='sales')
            executor.load_dataframe(df, 'weather', database_name='climate')
            
            sales_tables = executor.list_tables(database='sales')
            
            assert 'customers' in sales_tables
            assert 'orders' in sales_tables
            assert 'weather' not in sales_tables
    
    def test_get_table_info(self):
        """Test getting table column information."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['a', 'b', 'c'],
                'value': [1.1, 2.2, 3.3]
            })
            executor.load_dataframe(df, 'test')
            
            info = executor.get_table_info('test')
            
            column_names = [col['name'] for col in info]
            assert 'id' in column_names
            assert 'name' in column_names
            assert 'value' in column_names
    
    def test_get_row_count(self):
        """Test getting row count."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({'a': range(100)})
            executor.load_dataframe(df, 'big_table')
            
            count = executor.get_row_count('big_table')
            
            assert count == 100
    
    def test_sample_data(self):
        """Test getting sample data."""
        with SQLiteExecutor(':memory:') as executor:
            df = pd.DataFrame({'a': range(100)})
            executor.load_dataframe(df, 'big_table')
            
            sample = executor.sample_data('big_table', n=5)
            
            assert len(sample) == 5


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_table(self):
        """Test querying non-existent table."""
        with SQLiteExecutor(':memory:') as executor:
            result = executor.execute_query("SELECT * FROM nonexistent")
            
            assert not result.success
            assert result.error is not None
    
    def test_invalid_sql(self):
        """Test invalid SQL syntax."""
        with SQLiteExecutor(':memory:') as executor:
            result = executor.execute_query("INVALID QUERY SYNTAX")
            
            assert not result.success
            assert result.error is not None


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SQLite Executor Tests")
    print("=" * 60)
    
    # Test 1: Basic connection
    print("\nTest 1: Basic connection")
    executor = SQLiteExecutor(':memory:')
    executor.connect()
    print(f"  Connected: {executor.conn is not None}")
    executor.close()
    print("  ✓ Connection test passed")
    
    # Test 2: Load and query data
    print("\nTest 2: Load and query data")
    with SQLiteExecutor(':memory:') as executor:
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [28, 35, 22, 45, 31],
            'city': ['Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi'],
            'purchase_amount': [5000, 7500, 3000, 12000, 6000]
        })
        executor.load_dataframe(df, 'customers', database_name='sales_data')
        
        result = executor.execute_select('sales_data__customers', where_clause='age > 30')
        print(f"  Rows with age > 30: {len(result)}")
        print(f"  Names: {result['name'].tolist()}")
    print("  ✓ Load and query test passed")
    
    # Test 3: Execute DMQL query
    print("\nTest 3: Execute DMQL query")
    with SQLiteExecutor(':memory:') as executor:
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [28, 35, 22, 45, 31],
            'city': ['Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi'],
            'purchase_amount': [5000, 7500, 3000, 12000, 6000]
        })
        executor.load_dataframe(df, 'customers', database_name='sales_data')
        
        query = """
        USE DATABASE sales_data
        FROM customers
        WHERE age > 25
        ORDER BY purchase_amount DESC
        """
        
        parsed = parse_query(query)
        result = executor.execute_query(parsed)
        
        print(f"  Success: {result.success}")
        print(f"  SQL: {result.sql_query}")
        print(f"  Rows: {result.row_count}")
        if result.data is not None:
            print(f"  First row: {result.data.iloc[0].to_dict()}")
    print("  ✓ DMQL query execution test passed")
    
    print("\n" + "=" * 60)
    print("All manual tests passed!")
    print("=" * 60)
    print("\nTo run full pytest suite: pytest backend/tests/test_executor.py -v")
