"""
Clustering Operations for DMQL Mining

This module provides K-Means and other clustering algorithms
for use with DMQL MINE CLUSTER queries.

Usage:
    from backend.dqml.mining import kmeans_clustering
    
    df = pd.DataFrame(...)
    result_df = kmeans_clustering(df, n_clusters=5)
    # df now has 'cluster' column with cluster assignments
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from dataclasses import dataclass


@dataclass
class ClusteringResult:
    """Result of clustering operation."""
    data: pd.DataFrame  # DataFrame with cluster assignments
    n_clusters: int
    cluster_centers: Optional[np.ndarray] = None
    feature_columns: List[str] = None
    silhouette_score: Optional[float] = None
    cluster_sizes: Dict[int, int] = None
    inertia: Optional[float] = None  # For K-Means
    
    def __post_init__(self):
        if self.feature_columns is None:
            self.feature_columns = []
        if self.cluster_sizes is None:
            self.cluster_sizes = {}


def kmeans_clustering(
    df: pd.DataFrame,
    n_clusters: int = 5,
    feature_columns: Optional[List[str]] = None,
    scale_features: bool = True,
    random_state: int = 42
) -> ClusteringResult:
    """
    Perform K-Means clustering on a DataFrame.
    
    Args:
        df: Input DataFrame
        n_clusters: Number of clusters (K)
        feature_columns: Columns to use for clustering (None for auto-detect numeric)
        scale_features: Whether to standardize features before clustering
        random_state: Random seed for reproducibility
        
    Returns:
        ClusteringResult with clustered data and metadata
        
    Example:
        >>> df = pd.DataFrame({'age': [25, 30, 35], 'income': [50000, 60000, 70000]})
        >>> result = kmeans_clustering(df, n_clusters=2)
        >>> print(result.data['cluster'])
    """
    # Make a copy to avoid modifying original
    result_df = df.copy()
    
    # Auto-detect numeric columns if not specified
    if feature_columns is None:
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not feature_columns:
        raise ValueError("No numeric columns found for clustering")
    
    # Extract features
    X = df[feature_columns].values
    
    # Handle missing values
    X = np.nan_to_num(X, nan=0)
    
    # Scale features if requested
    scaler = None
    if scale_features:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X
    
    # Perform K-Means clustering
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to DataFrame
    result_df['cluster'] = cluster_labels
    
    # Calculate silhouette score if we have more than 1 cluster and enough samples
    silhouette = None
    if n_clusters > 1 and len(df) > n_clusters:
        try:
            silhouette = silhouette_score(X_scaled, cluster_labels)
        except:
            pass
    
    # Calculate cluster sizes
    cluster_sizes = dict(result_df['cluster'].value_counts())
    
    # Get cluster centers (unscaled if scaling was used)
    centers = kmeans.cluster_centers_
    if scale_features and scaler:
        centers = scaler.inverse_transform(centers)
    
    return ClusteringResult(
        data=result_df,
        n_clusters=n_clusters,
        cluster_centers=centers,
        feature_columns=feature_columns,
        silhouette_score=silhouette,
        cluster_sizes=cluster_sizes,
        inertia=kmeans.inertia_
    )


def dbscan_clustering(
    df: pd.DataFrame,
    eps: float = 0.5,
    min_samples: int = 5,
    feature_columns: Optional[List[str]] = None,
    scale_features: bool = True
) -> ClusteringResult:
    """
    Perform DBSCAN clustering on a DataFrame.
    
    DBSCAN automatically determines the number of clusters and can
    identify noise points (labeled as -1).
    
    Args:
        df: Input DataFrame
        eps: Maximum distance between samples in a neighborhood
        min_samples: Minimum samples in a neighborhood for a core point
        feature_columns: Columns to use for clustering
        scale_features: Whether to standardize features
        
    Returns:
        ClusteringResult with clustered data
    """
    result_df = df.copy()
    
    if feature_columns is None:
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not feature_columns:
        raise ValueError("No numeric columns found for clustering")
    
    X = df[feature_columns].values
    X = np.nan_to_num(X, nan=0)
    
    if scale_features:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X
    
    # Perform DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(X_scaled)
    
    result_df['cluster'] = cluster_labels
    
    # Count clusters (excluding noise labeled as -1)
    unique_labels = set(cluster_labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    
    # Calculate silhouette score, excluding noise points
    silhouette = None
    if n_clusters > 1:
        mask = cluster_labels != -1
        if mask.sum() > n_clusters:
            try:
                silhouette = silhouette_score(X_scaled[mask], cluster_labels[mask])
            except:
                pass
    
    cluster_sizes = dict(result_df['cluster'].value_counts())
    
    return ClusteringResult(
        data=result_df,
        n_clusters=n_clusters,
        feature_columns=feature_columns,
        silhouette_score=silhouette,
        cluster_sizes=cluster_sizes
    )


def hierarchical_clustering(
    df: pd.DataFrame,
    n_clusters: int = 5,
    feature_columns: Optional[List[str]] = None,
    linkage: str = 'ward',
    scale_features: bool = True
) -> ClusteringResult:
    """
    Perform hierarchical/agglomerative clustering on a DataFrame.
    
    Args:
        df: Input DataFrame
        n_clusters: Number of clusters
        feature_columns: Columns to use for clustering
        linkage: Linkage method ('ward', 'complete', 'average', 'single')
        scale_features: Whether to standardize features
        
    Returns:
        ClusteringResult with clustered data
    """
    result_df = df.copy()
    
    if feature_columns is None:
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not feature_columns:
        raise ValueError("No numeric columns found for clustering")
    
    X = df[feature_columns].values
    X = np.nan_to_num(X, nan=0)
    
    if scale_features:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X
    
    # Perform hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage
    )
    cluster_labels = clustering.fit_predict(X_scaled)
    
    result_df['cluster'] = cluster_labels
    
    silhouette = None
    if n_clusters > 1 and len(df) > n_clusters:
        try:
            silhouette = silhouette_score(X_scaled, cluster_labels)
        except:
            pass
    
    cluster_sizes = dict(result_df['cluster'].value_counts())
    
    return ClusteringResult(
        data=result_df,
        n_clusters=n_clusters,
        feature_columns=feature_columns,
        silhouette_score=silhouette,
        cluster_sizes=cluster_sizes
    )


def find_optimal_k(
    df: pd.DataFrame,
    k_range: Tuple[int, int] = (2, 10),
    feature_columns: Optional[List[str]] = None,
    scale_features: bool = True
) -> Dict[str, Any]:
    """
    Find the optimal number of clusters using the elbow method and silhouette score.
    
    Args:
        df: Input DataFrame
        k_range: Range of K values to try (min, max)
        feature_columns: Columns to use for clustering
        scale_features: Whether to standardize features
        
    Returns:
        Dictionary with optimal K and metrics for each K value
    """
    if feature_columns is None:
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    X = df[feature_columns].values
    X = np.nan_to_num(X, nan=0)
    
    if scale_features:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X
    
    results = {
        'k_values': [],
        'inertia': [],
        'silhouette_scores': []
    }
    
    for k in range(k_range[0], k_range[1] + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        
        results['k_values'].append(k)
        results['inertia'].append(kmeans.inertia_)
        
        if k > 1:
            try:
                score = silhouette_score(X_scaled, labels)
                results['silhouette_scores'].append(score)
            except:
                results['silhouette_scores'].append(0)
        else:
            results['silhouette_scores'].append(0)
    
    # Find optimal K based on silhouette score
    if results['silhouette_scores']:
        best_idx = np.argmax(results['silhouette_scores'])
        results['optimal_k'] = results['k_values'][best_idx]
        results['best_silhouette'] = results['silhouette_scores'][best_idx]
    else:
        results['optimal_k'] = k_range[0]
        results['best_silhouette'] = 0
    
    return results
