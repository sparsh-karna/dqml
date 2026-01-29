# DQML Parser Package
"""
DQML Parser - ANTLR4 generated lexer and parser for DMQL queries.

Usage:
    from backend.dqml.parser import parse_query
    
    query = '''
    USE DATABASE sales_data
    FROM customers
    WHERE age > 25
    '''
    ast = parse_query(query)
"""

from .dmql_parser import parse_query, DMQLQueryVisitor

__all__ = ['parse_query', 'DMQLQueryVisitor']
