# DQML Executor Package
"""
DQML Executor - Query execution engine for DMQL queries.

Supports:
- SQLite backend (default)
- DuckDB backend (faster analytics)
"""

from .sqlite_executor import SQLiteExecutor, ExecutionResult

__all__ = ['SQLiteExecutor', 'ExecutionResult']
