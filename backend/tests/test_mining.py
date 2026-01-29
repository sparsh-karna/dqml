"""
Tests for DMQL Mining Operations
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
import pytest

from backend.dqml.mining import (
    kmeans_clustering,
    basic_statistics,
    detect_anomalies,
    data_profile
)


class TestClustering:
    """Test clustering operations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        return pd.DataFrame({
            'x': np.concatenate([
                np.random.normal(0, 1, 30),
                np.random.normal(5, 1, 30),
                np.random.normal(10, 1, 30)
            ]),
            'y': np.concatenate([
                np.random.normal(0, 1, 30),
                np.random.normal(5, 1, 30),
                np.random.normal(0, 1, 30)
            ])
        })
    
    def test_kmeans_basic(self, sample_data):
        """Test basic K-means clustering."""
        result = kmeans_clustering(sample_data, n_clusters=3)
        
        assert result.n_clusters == 3
        assert 'cluster' in result.data.columns
        assert len(result.data) == len(sample_data)
        assert result.cluster_centers is not None
        assert len(result.cluster_centers) == 3
    
    def test_kmeans_silhouette(self, sample_data):
        """Test that silhouette score is calculated."""
        result = kmeans_clustering(sample_data, n_clusters=3)
        
        assert result.silhouette_score is not None
        assert -1 <= result.silhouette_score <= 1
    
    def test_kmeans_cluster_sizes(self, sample_data):
        """Test cluster sizes are reported."""
        result = kmeans_clustering(sample_data, n_clusters=3)
        
        assert result.cluster_sizes is not None
        total = sum(result.cluster_sizes.values())
        assert total == len(sample_data)


class TestStatistics:
    """Test statistics operations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'income': [50000, 60000, 70000, 80000, 90000],
            'city': ['A', 'B', 'A', 'C', 'B']
        })
    
    def test_basic_statistics(self, sample_data):
        """Test basic statistics calculation."""
        stats = basic_statistics(sample_data)
        
        assert stats.count == 5
        assert 'age' in stats.numeric_columns
        assert 'income' in stats.numeric_columns
        assert 'city' in stats.categorical_columns
    
    def test_statistics_values(self, sample_data):
        """Test that statistics values are correct."""
        stats = basic_statistics(sample_data)
        
        assert stats.summary['age']['mean'] == 35.0
        assert stats.summary['age']['min'] == 25.0
        assert stats.summary['age']['max'] == 45.0
    
    def test_data_profile(self, sample_data):
        """Test data profiling."""
        profile = data_profile(sample_data)
        
        assert profile['row_count'] == 5
        assert profile['column_count'] == 3
        assert 'age' in profile['columns']
        assert 'data_quality_score' in profile


class TestAnomalyDetection:
    """Test anomaly detection operations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with anomalies."""
        np.random.seed(42)
        data = pd.DataFrame({
            'value': np.random.normal(50, 10, 100)
        })
        # Add outliers
        data.loc[0, 'value'] = 200
        data.loc[1, 'value'] = -100
        return data
    
    def test_isolation_forest(self, sample_data):
        """Test Isolation Forest anomaly detection."""
        result = detect_anomalies(
            sample_data, 
            method='isolation_forest',
            contamination=0.05
        )
        
        assert 'is_anomaly' in result.data.columns
        assert result.n_anomalies > 0
        assert result.method == 'isolation_forest'
    
    def test_iqr_detection(self, sample_data):
        """Test IQR-based anomaly detection."""
        result = detect_anomalies(sample_data, method='iqr')
        
        assert 'is_anomaly' in result.data.columns
        assert result.n_anomalies >= 2  # Should detect our outliers
    
    def test_zscore_detection(self, sample_data):
        """Test Z-score anomaly detection."""
        result = detect_anomalies(sample_data, method='zscore')
        
        assert 'is_anomaly' in result.data.columns
        assert result.method == 'zscore'


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Mining Operations Tests")
    print("=" * 60)
    
    # Test data
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    # Add an anomaly
    df.loc[0, 'x'] = 100
    
    # Test 1: Clustering
    print("\nTest 1: K-Means Clustering")
    result = kmeans_clustering(df, n_clusters=3)
    print(f"  Clusters: {result.n_clusters}")
    print(f"  Silhouette Score: {result.silhouette_score:.4f}")
    print("  ✓ Clustering passed")
    
    # Test 2: Statistics
    print("\nTest 2: Basic Statistics")
    stats = basic_statistics(df)
    print(f"  Row count: {stats.count}")
    print(f"  Numeric columns: {stats.numeric_columns}")
    print(f"  Mean of x: {stats.summary['x']['mean']:.4f}")
    print("  ✓ Statistics passed")
    
    # Test 3: Anomaly Detection
    print("\nTest 3: Anomaly Detection")
    anomaly = detect_anomalies(df, method='isolation_forest', contamination=0.05)
    print(f"  Anomalies found: {anomaly.n_anomalies}")
    print(f"  Anomaly %: {anomaly.anomaly_percentage}%")
    print("  ✓ Anomaly detection passed")
    
    # Test 4: Data Profile
    print("\nTest 4: Data Profile")
    profile = data_profile(df)
    print(f"  Quality score: {profile['data_quality_score']}%")
    print("  ✓ Data profiling passed")
    
    print("\n" + "=" * 60)
    print("All manual tests passed!")
    print("=" * 60)
    print("\nTo run full pytest suite: pytest backend/tests/test_mining.py -v")
