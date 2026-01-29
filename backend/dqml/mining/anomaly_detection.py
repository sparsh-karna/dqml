"""
Anomaly Detection Operations for DMQL Mining

This module provides anomaly detection algorithms for use with
DMQL MINE ANOMALIES queries.

Usage:
    from backend.dqml.mining.anomaly_detection import detect_anomalies
    
    df = pd.DataFrame(...)
    result = detect_anomalies(df)
    print(result.data['is_anomaly'])
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from dataclasses import dataclass, field


@dataclass
class AnomalyResult:
    """Result of anomaly detection operation."""
    data: pd.DataFrame  # DataFrame with anomaly labels
    n_anomalies: int
    anomaly_percentage: float
    feature_columns: List[str] = field(default_factory=list)
    anomaly_scores: Optional[np.ndarray] = None
    threshold: Optional[float] = None
    method: str = 'isolation_forest'
    
    def get_anomalies(self) -> pd.DataFrame:
        """Get only the anomalous rows."""
        return self.data[self.data['is_anomaly'] == True]
    
    def get_normal(self) -> pd.DataFrame:
        """Get only the normal rows."""
        return self.data[self.data['is_anomaly'] == False]


def detect_anomalies(
    df: pd.DataFrame,
    method: str = 'isolation_forest',
    contamination: float = 0.1,
    feature_columns: Optional[List[str]] = None,
    scale_features: bool = True,
    random_state: int = 42
) -> AnomalyResult:
    """
    Detect anomalies in a DataFrame using various methods.
    
    Args:
        df: Input DataFrame
        method: Detection method ('isolation_forest', 'lof', 'zscore', 'iqr')
        contamination: Expected proportion of anomalies (for ML methods)
        feature_columns: Columns to use for detection (None for auto-detect)
        scale_features: Whether to standardize features
        random_state: Random seed for reproducibility
        
    Returns:
        AnomalyResult with labeled data and metadata
        
    Example:
        >>> df = pd.DataFrame({'value': [1, 2, 3, 100, 4, 5]})
        >>> result = detect_anomalies(df, method='iqr')
        >>> print(result.data['is_anomaly'])
    """
    result_df = df.copy()
    
    # Auto-detect numeric columns if not specified
    if feature_columns is None:
        feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not feature_columns:
        raise ValueError("No numeric columns found for anomaly detection")
    
    # Select detection method
    if method == 'isolation_forest':
        return _isolation_forest_detection(
            df, feature_columns, contamination, scale_features, random_state
        )
    elif method == 'lof':
        return _lof_detection(
            df, feature_columns, contamination, scale_features
        )
    elif method == 'zscore':
        return _zscore_detection(df, feature_columns, threshold=3.0)
    elif method == 'iqr':
        return _iqr_detection(df, feature_columns)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'isolation_forest', 'lof', 'zscore', or 'iqr'")


def _isolation_forest_detection(
    df: pd.DataFrame,
    feature_columns: List[str],
    contamination: float,
    scale_features: bool,
    random_state: int
) -> AnomalyResult:
    """Detect anomalies using Isolation Forest."""
    result_df = df.copy()
    X = df[feature_columns].values
    X = np.nan_to_num(X, nan=0)
    
    if scale_features:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    # Fit Isolation Forest
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=100
    )
    
    # Predict: -1 for anomalies, 1 for normal
    predictions = iso_forest.fit_predict(X)
    scores = iso_forest.decision_function(X)
    
    result_df['is_anomaly'] = predictions == -1
    result_df['anomaly_score'] = -scores  # Higher score = more anomalous
    
    n_anomalies = int((predictions == -1).sum())
    
    return AnomalyResult(
        data=result_df,
        n_anomalies=n_anomalies,
        anomaly_percentage=round(n_anomalies / len(df) * 100, 2),
        feature_columns=feature_columns,
        anomaly_scores=-scores,
        method='isolation_forest'
    )


def _lof_detection(
    df: pd.DataFrame,
    feature_columns: List[str],
    contamination: float,
    scale_features: bool
) -> AnomalyResult:
    """Detect anomalies using Local Outlier Factor."""
    result_df = df.copy()
    X = df[feature_columns].values
    X = np.nan_to_num(X, nan=0)
    
    if scale_features:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    # Fit LOF
    lof = LocalOutlierFactor(
        contamination=contamination,
        n_neighbors=min(20, len(df) - 1)
    )
    
    # Predict: -1 for anomalies, 1 for normal
    predictions = lof.fit_predict(X)
    scores = -lof.negative_outlier_factor_  # Higher = more anomalous
    
    result_df['is_anomaly'] = predictions == -1
    result_df['anomaly_score'] = scores
    
    n_anomalies = int((predictions == -1).sum())
    
    return AnomalyResult(
        data=result_df,
        n_anomalies=n_anomalies,
        anomaly_percentage=round(n_anomalies / len(df) * 100, 2),
        feature_columns=feature_columns,
        anomaly_scores=scores,
        method='lof'
    )


def _zscore_detection(
    df: pd.DataFrame,
    feature_columns: List[str],
    threshold: float = 3.0
) -> AnomalyResult:
    """
    Detect anomalies using Z-score method.
    
    Points with Z-score > threshold in any feature are flagged as anomalies.
    """
    result_df = df.copy()
    X = df[feature_columns].copy()
    
    # Calculate Z-scores
    zscores = np.abs((X - X.mean()) / X.std())
    
    # Flag as anomaly if any feature exceeds threshold
    is_anomaly = (zscores > threshold).any(axis=1)
    max_zscore = zscores.max(axis=1)
    
    result_df['is_anomaly'] = is_anomaly
    result_df['anomaly_score'] = max_zscore
    
    n_anomalies = int(is_anomaly.sum())
    
    return AnomalyResult(
        data=result_df,
        n_anomalies=n_anomalies,
        anomaly_percentage=round(n_anomalies / len(df) * 100, 2),
        feature_columns=feature_columns,
        anomaly_scores=max_zscore.values,
        threshold=threshold,
        method='zscore'
    )


def _iqr_detection(
    df: pd.DataFrame,
    feature_columns: List[str],
    multiplier: float = 1.5
) -> AnomalyResult:
    """
    Detect anomalies using the IQR (Interquartile Range) method.
    
    Points outside [Q1 - multiplier*IQR, Q3 + multiplier*IQR] are anomalies.
    """
    result_df = df.copy()
    X = df[feature_columns]
    
    # Calculate IQR bounds for each feature
    Q1 = X.quantile(0.25)
    Q3 = X.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    # Flag as anomaly if any feature is outside bounds
    is_below = X < lower_bound
    is_above = X > upper_bound
    is_anomaly = (is_below | is_above).any(axis=1)
    
    # Calculate anomaly score as max distance from bounds (normalized)
    below_distance = (lower_bound - X).clip(lower=0) / IQR
    above_distance = (X - upper_bound).clip(lower=0) / IQR
    anomaly_score = (below_distance.abs().max(axis=1) + above_distance.abs().max(axis=1))
    
    result_df['is_anomaly'] = is_anomaly
    result_df['anomaly_score'] = anomaly_score
    
    n_anomalies = int(is_anomaly.sum())
    
    return AnomalyResult(
        data=result_df,
        n_anomalies=n_anomalies,
        anomaly_percentage=round(n_anomalies / len(df) * 100, 2),
        feature_columns=feature_columns,
        anomaly_scores=anomaly_score.values,
        method='iqr'
    )


def detect_univariate_anomalies(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr',
    threshold: float = None
) -> Dict[str, Any]:
    """
    Detect anomalies in a single column.
    
    Args:
        df: Input DataFrame
        column: Column to analyze
        method: Detection method ('iqr', 'zscore', 'mad')
        threshold: Custom threshold (method-specific)
        
    Returns:
        Dictionary with anomaly information
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    col_data = df[column].dropna()
    
    if not np.issubdtype(col_data.dtype, np.number):
        raise ValueError(f"Column '{column}' is not numeric")
    
    if method == 'iqr':
        multiplier = threshold or 1.5
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        anomalies = col_data[(col_data < lower) | (col_data > upper)]
        
    elif method == 'zscore':
        z_threshold = threshold or 3.0
        z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
        anomalies = col_data[z_scores > z_threshold]
        lower = col_data.mean() - z_threshold * col_data.std()
        upper = col_data.mean() + z_threshold * col_data.std()
        
    elif method == 'mad':
        # Median Absolute Deviation
        mad_threshold = threshold or 3.5
        median = col_data.median()
        mad = np.median(np.abs(col_data - median))
        modified_z = 0.6745 * (col_data - median) / mad if mad > 0 else pd.Series([0] * len(col_data))
        anomalies = col_data[np.abs(modified_z) > mad_threshold]
        lower = median - mad_threshold * mad / 0.6745
        upper = median + mad_threshold * mad / 0.6745
        
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return {
        'column': column,
        'method': method,
        'n_total': len(col_data),
        'n_anomalies': len(anomalies),
        'anomaly_percentage': round(len(anomalies) / len(col_data) * 100, 2) if len(col_data) > 0 else 0,
        'lower_bound': float(lower),
        'upper_bound': float(upper),
        'anomaly_indices': anomalies.index.tolist(),
        'anomaly_values': anomalies.tolist()
    }
