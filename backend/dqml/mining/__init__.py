# DQML Mining Package
"""
DQML Mining - Data mining algorithms for DMQL queries.

Supported Operations:
- Clustering (K-Means, DBSCAN, Hierarchical)
- Basic Statistics
- Anomaly Detection (Isolation Forest, LOF, Z-Score, IQR)
- Association Rules (planned)
"""

from .clustering import (
    kmeans_clustering,
    dbscan_clustering,
    hierarchical_clustering,
    find_optimal_k,
    ClusteringResult
)

from .statistics import (
    basic_statistics,
    column_statistics,
    correlation_analysis,
    distribution_analysis,
    group_statistics,
    data_profile,
    StatisticsResult
)

from .anomaly_detection import (
    detect_anomalies,
    detect_univariate_anomalies,
    AnomalyResult
)

__all__ = [
    # Clustering
    'kmeans_clustering',
    'dbscan_clustering',
    'hierarchical_clustering',
    'find_optimal_k',
    'ClusteringResult',
    # Statistics
    'basic_statistics',
    'column_statistics',
    'correlation_analysis',
    'distribution_analysis',
    'group_statistics',
    'data_profile',
    'StatisticsResult',
    # Anomaly Detection
    'detect_anomalies',
    'detect_univariate_anomalies',
    'AnomalyResult'
]
