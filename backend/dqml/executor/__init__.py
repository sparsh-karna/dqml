# DQML Executor Package
"""
DQML Executor - Query execution engine for DMQL queries.

Supports:
- SQLite backend (default)
- DuckDB backend (faster analytics)
"""

from .sqlite_executor import SQLiteExecutor

__all__ = ['SQLiteExecutor']
