"""
SQLite Executor for DMQL Queries

This module translates parsed DMQL queries into SQL and executes them
against a SQLite database backend.

Usage:
    from backend.dqml.executor import SQLiteExecutor
    
    executor = SQLiteExecutor()
    executor.connect(':memory:')
    executor.load_csv('data/customers.csv', 'customers')
    
    result = executor.execute_query(parsed_query)
"""

import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass

# Import parser types
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.dqml.parser.dmql_parser import DMQLQuery, Condition


@dataclass
class ExecutionResult:
    """Result of query execution."""
    success: bool
    data: Optional[pd.DataFrame] = None
    sql_query: str = ''
    row_count: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SQLiteExecutor:
    """
    Executes DMQL queries against a SQLite database.
    
    This executor:
    - Translates DMQL queries to SQL
    - Manages database connections
    - Loads CSV data into tables
    - Returns results as pandas DataFrames
    """
    
    def __init__(self, db_path: str = ':memory:'):
        """
        Initialize the SQLite executor.
        
        Args:
            db_path: Path to SQLite database file, or ':memory:' for in-memory DB
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._databases: Dict[str, str] = {}  # Maps database names to table prefixes
        self._current_database: Optional[str] = None
    
    def connect(self, db_path: Optional[str] = None) -> 'SQLiteExecutor':
        """
        Connect to the SQLite database.
        
        Args:
            db_path: Optional path to override the default database path
            
        Returns:
            Self for method chaining
        """
        if db_path:
            self.db_path = db_path
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        return self
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    # ========================================================================
    # DATA LOADING
    # ========================================================================
    
    def load_csv(self, csv_path: str, table_name: str, 
                 database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Load a CSV file into a SQLite table.
        
        Args:
            csv_path: Path to the CSV file
            table_name: Name for the table in SQLite
            database_name: Optional database name for organizing tables
            
        Returns:
            The loaded DataFrame
        """
        if not self.conn:
            self.connect()
        
        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)
        
        # Create full table name with database prefix if provided
        full_table_name = table_name
        if database_name:
            full_table_name = f"{database_name}__{table_name}"
            if database_name not in self._databases:
                self._databases[database_name] = database_name
        
        # Load into SQLite
        df.to_sql(full_table_name, self.conn, if_exists='replace', index=False)
        
        return df
    
    def load_dataframe(self, df: pd.DataFrame, table_name: str,
                       database_name: Optional[str] = None) -> None:
        """
        Load a pandas DataFrame into a SQLite table.
        
        Args:
            df: The DataFrame to load
            table_name: Name for the table
            database_name: Optional database name
        """
        if not self.conn:
            self.connect()
        
        full_table_name = table_name
        if database_name:
            full_table_name = f"{database_name}__{table_name}"
            if database_name not in self._databases:
                self._databases[database_name] = database_name
        
        df.to_sql(full_table_name, self.conn, if_exists='replace', index=False)
    
    def register_database(self, name: str, tables_path: Optional[str] = None) -> None:
        """
        Register a database name for organizing tables.
        
        Args:
            name: The database name
            tables_path: Optional path to directory containing CSV files
        """
        self._databases[name] = name
        
        if tables_path:
            path = Path(tables_path)
            if path.is_dir():
                for csv_file in path.glob('*.csv'):
                    table_name = csv_file.stem
                    self.load_csv(str(csv_file), table_name, database_name=name)
    
    def use_database(self, name: str) -> None:
        """Set the current database context."""
        self._current_database = name
    
    # ========================================================================
    # QUERY EXECUTION
    # ========================================================================
    
    def execute_query(self, query: Union[DMQLQuery, str]) -> ExecutionResult:
        """
        Execute a DMQL query and return results.
        
        Args:
            query: Either a parsed DMQLQuery object or a raw SQL string
            
        Returns:
            ExecutionResult with data and metadata
        """
        if not self.conn:
            self.connect()
        
        # If raw SQL string, execute directly
        if isinstance(query, str):
            return self._execute_raw_sql(query)
        
        # Translate DMQL to SQL
        sql = self._translate_to_sql(query)
        
        # Execute the SQL
        try:
            df = pd.read_sql_query(sql, self.conn)
            
            return ExecutionResult(
                success=True,
                data=df,
                sql_query=sql,
                row_count=len(df),
                metadata={
                    'database': query.database,
                    'tables': query.tables,
                    'columns': list(df.columns) if df is not None else []
                }
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                sql_query=sql,
                error=str(e)
            )
    
    def _execute_raw_sql(self, sql: str) -> ExecutionResult:
        """Execute raw SQL and return results."""
        try:
            df = pd.read_sql_query(sql, self.conn)
            return ExecutionResult(
                success=True,
                data=df,
                sql_query=sql,
                row_count=len(df)
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                sql_query=sql,
                error=str(e)
            )
    
    def execute_select(self, table: str, columns: Optional[List[str]] = None,
                       where_clause: Optional[str] = None,
                       group_by: Optional[List[str]] = None,
                       order_by: Optional[List[tuple]] = None,
                       limit: Optional[int] = None) -> pd.DataFrame:
        """
        Execute a simple SELECT query.
        
        Args:
            table: Table name
            columns: List of columns to select (None for all)
            where_clause: WHERE condition string
            group_by: List of columns for GROUP BY
            order_by: List of (column, direction) tuples
            limit: Maximum rows to return
            
        Returns:
            DataFrame with query results
        """
        if not self.conn:
            self.connect()
        
        # Build column list
        cols = '*' if not columns else ', '.join(columns)
        
        # Build query
        sql = f"SELECT {cols} FROM {table}"
        
        if where_clause:
            sql += f" WHERE {where_clause}"
        
        if group_by:
            sql += f" GROUP BY {', '.join(group_by)}"
        
        if order_by:
            order_parts = [f"{col} {direction}" for col, direction in order_by]
            sql += f" ORDER BY {', '.join(order_parts)}"
        
        if limit:
            sql += f" LIMIT {limit}"
        
        return pd.read_sql_query(sql, self.conn)
    
    # ========================================================================
    # DMQL TO SQL TRANSLATION
    # ========================================================================
    
    def _translate_to_sql(self, query: DMQLQuery) -> str:
        """
        Translate a DMQL query to SQL.
        
        Args:
            query: Parsed DMQL query
            
        Returns:
            SQL string
        """
        # Determine table names with potential database prefix
        tables = self._get_table_names(query.database, query.tables)
        
        # Build SELECT clause
        if query.columns:
            columns = ', '.join(query.columns)
        else:
            columns = '*'
        
        # Start building SQL
        sql = f"SELECT {columns} FROM {', '.join(tables)}"
        
        # Add WHERE clause
        if query.conditions:
            where_sql = self._condition_to_sql(query.conditions)
            sql += f" WHERE {where_sql}"
        
        # Add GROUP BY
        if query.group_by:
            sql += f" GROUP BY {', '.join(query.group_by)}"
        
        # Add ORDER BY
        if query.order_by:
            order_parts = [f"{col} {direction}" for col, direction in query.order_by]
            sql += f" ORDER BY {', '.join(order_parts)}"
        
        return sql
    
    def _get_table_names(self, database: str, tables: List[str]) -> List[str]:
        """
        Get the actual table names, potentially with database prefix.
        
        Args:
            database: Database name from query
            tables: List of table names from query
            
        Returns:
            List of actual table names in SQLite
        """
        result = []
        for table in tables:
            # Check if table exists with database prefix
            prefixed_name = f"{database}__{table}"
            if self._table_exists(prefixed_name):
                result.append(prefixed_name)
            elif self._table_exists(table):
                result.append(table)
            else:
                # Table doesn't exist, use as-is (will error on execution)
                result.append(table)
        return result
    
    def _table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        if not self.conn:
            return False
        
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None
    
    def _condition_to_sql(self, condition: Condition) -> str:
        """
        Convert a Condition object to SQL WHERE clause.
        
        Args:
            condition: Condition object from parsed query
            
        Returns:
            SQL condition string
        """
        # Handle nested conditions (AND/OR)
        if condition.nested:
            parts = [self._condition_to_sql(c) for c in condition.nested]
            op = condition.logical_op or 'AND'
            return f"({f' {op} '.join(parts)})"
        
        # Handle simple conditions
        left = condition.left
        operator = condition.operator
        right = condition.right
        
        # Format the right side based on type
        if isinstance(right, str):
            right_sql = f"'{right}'"
        elif right is None:
            right_sql = 'NULL'
        else:
            right_sql = str(right)
        
        return f"{left} {operator} {right_sql}"
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about a table's columns.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column info dictionaries
        """
        if not self.conn:
            self.connect()
        
        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        return [
            {
                'name': col[1],
                'type': col[2],
                'notnull': bool(col[3]),
                'default': col[4],
                'primary_key': bool(col[5])
            }
            for col in columns
        ]
    
    def list_tables(self, database: Optional[str] = None) -> List[str]:
        """
        List all tables in the database.
        
        Args:
            database: Optional database name to filter by
            
        Returns:
            List of table names
        """
        if not self.conn:
            self.connect()
        
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        
        # Filter by database prefix if specified
        if database:
            prefix = f"{database}__"
            tables = [t for t in tables if t.startswith(prefix)]
            # Remove the prefix for display
            tables = [t[len(prefix):] for t in tables]
        
        return tables
    
    def get_row_count(self, table_name: str) -> int:
        """Get the number of rows in a table."""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    
    def sample_data(self, table_name: str, n: int = 5) -> pd.DataFrame:
        """Get sample rows from a table."""
        if not self.conn:
            self.connect()
        
        return pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {n}", self.conn)
