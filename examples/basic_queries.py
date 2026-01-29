#!/usr/bin/env python3
"""
DQML Basic Queries Example

Demonstrates basic SELECT, filter, and visualization queries.
"""

import requests
import json

API_URL = "http://localhost:8000"


def execute_query(query: str) -> dict:
    """Execute a DMQL query and return results."""
    response = requests.post(
        f"{API_URL}/api/execute",
        json={"query": query}
    )
    return response.json()


def load_sample_data():
    """Load sample customer data."""
    import os
    data_path = os.path.join(os.path.dirname(__file__), "../data/sample_customers.csv")
    data_path = os.path.abspath(data_path)
    
    response = requests.post(
        f"{API_URL}/api/load-csv",
        json={"file_path": data_path, "table_name": "customers"}
    )
    result = response.json()
    print(f"Loaded {result.get('row_count', 0)} rows into 'customers' table")
    return result


def main():
    print("=" * 60)
    print("DQML Basic Queries Example")
    print("=" * 60)
    
    # Load sample data
    print("\n1. Loading sample data...")
    load_sample_data()
    
    # Query 1: Select all
    print("\n2. Query: FROM customers")
    result = execute_query("FROM customers")
    print(f"   Rows returned: {result['row_count']}")
    print(f"   Columns: {result['columns']}")
    
    # Query 2: Filter by age
    print("\n3. Query: FROM customers WHERE age > 40")
    result = execute_query("FROM customers WHERE age > 40")
    print(f"   Rows returned: {result['row_count']}")
    if result['data']:
        print(f"   Sample: {result['data'][0]}")
    
    # Query 3: Filter by region
    print("\n4. Query: FROM customers WHERE region = 'North'")
    result = execute_query("FROM customers WHERE region = 'North'")
    print(f"   Rows returned: {result['row_count']}")
    
    # Query 4: Filter by income
    print("\n5. Query: FROM customers WHERE income > 80000")
    result = execute_query("FROM customers WHERE income > 80000")
    print(f"   Rows returned: {result['row_count']}")
    if result['data']:
        names = [row['name'] for row in result['data'][:5]]
        print(f"   High earners: {', '.join(names)}")
    
    print("\n" + "=" * 60)
    print("Basic queries complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
