"""
Statistical Operations for DMQL Mining

This module provides basic statistics and descriptive analysis
for use with DMQL MINE STATISTICS queries.

Usage:
    from backend.dqml.mining import basic_statistics
    
    df = pd.DataFrame(...)
    stats = basic_statistics(df)
    print(stats['summary'])
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from scipy import stats as scipy_stats


@dataclass
class StatisticsResult:
    """Result of statistical analysis."""
    count: int
    numeric_columns: List[str] = field(default_factory=list)
    categorical_columns: List[str] = field(default_factory=list)
    summary: Dict[str, Dict[str, float]] = field(default_factory=dict)
    correlations: Optional[pd.DataFrame] = None
    value_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    missing_values: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'count': self.count,
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'summary': self.summary,
            'correlations': self.correlations.to_dict() if self.correlations is not None else None,
            'value_counts': self.value_counts,
            'missing_values': self.missing_values
        }


def basic_statistics(df: pd.DataFrame) -> StatisticsResult:
    """
    Calculate basic statistics for a DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        StatisticsResult containing comprehensive statistics
        
    Example:
        >>> df = pd.DataFrame({'age': [25, 30, 35], 'name': ['A', 'B', 'C']})
        >>> stats = basic_statistics(df)
        >>> print(stats.summary['age']['mean'])
    """
    # Identify column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Calculate summary statistics for numeric columns
    summary = {}
    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) > 0:
            summary[col] = {
                'count': int(len(col_data)),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()) if len(col_data) > 1 else 0.0,
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'q25': float(col_data.quantile(0.25)),
                'q50': float(col_data.quantile(0.50)),
                'q75': float(col_data.quantile(0.75)),
                'variance': float(col_data.var()) if len(col_data) > 1 else 0.0,
                'skewness': float(col_data.skew()) if len(col_data) > 2 else 0.0,
                'kurtosis': float(col_data.kurtosis()) if len(col_data) > 3 else 0.0
            }
    
    # Calculate correlations for numeric columns
    correlations = None
    if len(numeric_cols) > 1:
        correlations = df[numeric_cols].corr()
    
    # Calculate value counts for categorical columns
    value_counts = {}
    for col in categorical_cols:
        counts = df[col].value_counts().head(20)  # Top 20 values
        value_counts[col] = counts.to_dict()
    
    # Calculate missing values
    missing_values = df.isnull().sum().to_dict()
    missing_values = {k: int(v) for k, v in missing_values.items() if v > 0}
    
    return StatisticsResult(
        count=len(df),
        numeric_columns=numeric_cols,
        categorical_columns=categorical_cols,
        summary=summary,
        correlations=correlations,
        value_counts=value_counts,
        missing_values=missing_values
    )


def column_statistics(
    df: pd.DataFrame,
    column: str
) -> Dict[str, Any]:
    """
    Calculate detailed statistics for a single column.
    
    Args:
        df: Input DataFrame
        column: Column name to analyze
        
    Returns:
        Dictionary with detailed statistics
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    col_data = df[column]
    
    result = {
        'column_name': column,
        'dtype': str(col_data.dtype),
        'count': int(len(col_data)),
        'non_null_count': int(col_data.notna().sum()),
        'null_count': int(col_data.isna().sum()),
        'unique_count': int(col_data.nunique())
    }
    
    # Numeric column statistics
    if np.issubdtype(col_data.dtype, np.number):
        clean_data = col_data.dropna()
        if len(clean_data) > 0:
            result.update({
                'mean': float(clean_data.mean()),
                'median': float(clean_data.median()),
                'std': float(clean_data.std()) if len(clean_data) > 1 else 0.0,
                'min': float(clean_data.min()),
                'max': float(clean_data.max()),
                'range': float(clean_data.max() - clean_data.min()),
                'q25': float(clean_data.quantile(0.25)),
                'q50': float(clean_data.quantile(0.50)),
                'q75': float(clean_data.quantile(0.75)),
                'iqr': float(clean_data.quantile(0.75) - clean_data.quantile(0.25)),
                'variance': float(clean_data.var()) if len(clean_data) > 1 else 0.0,
                'skewness': float(clean_data.skew()) if len(clean_data) > 2 else 0.0,
                'kurtosis': float(clean_data.kurtosis()) if len(clean_data) > 3 else 0.0
            })
            
            # Detect outliers using IQR method
            q1 = clean_data.quantile(0.25)
            q3 = clean_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)]
            result['outlier_count'] = int(len(outliers))
    else:
        # Categorical column statistics
        value_counts = col_data.value_counts().head(20)
        result['top_values'] = value_counts.to_dict()
        result['most_common'] = str(value_counts.index[0]) if len(value_counts) > 0 else None
        result['most_common_count'] = int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
    
    return result


def correlation_analysis(
    df: pd.DataFrame,
    method: str = 'pearson',
    threshold: float = 0.0
) -> Dict[str, Any]:
    """
    Perform correlation analysis on numeric columns.
    
    Args:
        df: Input DataFrame
        method: Correlation method ('pearson', 'spearman', 'kendall')
        threshold: Minimum absolute correlation to include
        
    Returns:
        Dictionary with correlation matrix and significant correlations
    """
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        return {'error': 'Need at least 2 numeric columns for correlation'}
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr(method=method)
    
    # Find significant correlations
    significant_correlations = []
    for i, col1 in enumerate(corr_matrix.columns):
        for j, col2 in enumerate(corr_matrix.columns):
            if i < j:  # Only upper triangle, excluding diagonal
                corr_value = corr_matrix.loc[col1, col2]
                if abs(corr_value) >= threshold:
                    significant_correlations.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': round(corr_value, 4),
                        'strength': _correlation_strength(corr_value)
                    })
    
    # Sort by absolute correlation value
    significant_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
    
    return {
        'method': method,
        'correlation_matrix': corr_matrix.to_dict(),
        'significant_correlations': significant_correlations,
        'columns': list(corr_matrix.columns)
    }


def _correlation_strength(corr: float) -> str:
    """Classify correlation strength."""
    abs_corr = abs(corr)
    if abs_corr >= 0.8:
        return 'very strong'
    elif abs_corr >= 0.6:
        return 'strong'
    elif abs_corr >= 0.4:
        return 'moderate'
    elif abs_corr >= 0.2:
        return 'weak'
    else:
        return 'very weak'


def distribution_analysis(
    df: pd.DataFrame,
    column: str,
    bins: int = 20
) -> Dict[str, Any]:
    """
    Analyze the distribution of a numeric column.
    
    Args:
        df: Input DataFrame
        column: Column to analyze
        bins: Number of bins for histogram
        
    Returns:
        Dictionary with distribution information
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
    
    col_data = df[column].dropna()
    
    if not np.issubdtype(col_data.dtype, np.number):
        raise ValueError(f"Column '{column}' is not numeric")
    
    # Calculate histogram
    hist_values, bin_edges = np.histogram(col_data, bins=bins)
    
    # Normality test (Shapiro-Wilk if sample is small, otherwise D'Agostino-Pearson)
    normality_test = None
    if len(col_data) >= 8:  # Minimum sample size for tests
        try:
            if len(col_data) <= 5000:
                stat, p_value = scipy_stats.shapiro(col_data)
                test_name = 'Shapiro-Wilk'
            else:
                stat, p_value = scipy_stats.normaltest(col_data)
                test_name = "D'Agostino-Pearson"
            
            normality_test = {
                'test_name': test_name,
                'statistic': float(stat),
                'p_value': float(p_value),
                'is_normal': p_value > 0.05
            }
        except:
            pass
    
    return {
        'column': column,
        'histogram': {
            'values': hist_values.tolist(),
            'bin_edges': bin_edges.tolist()
        },
        'normality_test': normality_test,
        'statistics': {
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'mode': float(col_data.mode().iloc[0]) if len(col_data.mode()) > 0 else None,
            'std': float(col_data.std()),
            'skewness': float(col_data.skew()),
            'kurtosis': float(col_data.kurtosis())
        }
    }


def group_statistics(
    df: pd.DataFrame,
    group_by: Union[str, List[str]],
    numeric_columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Calculate statistics grouped by one or more columns.
    
    Args:
        df: Input DataFrame
        group_by: Column(s) to group by
        numeric_columns: Numeric columns to aggregate (None for all)
        
    Returns:
        Dictionary with grouped statistics
    """
    if isinstance(group_by, str):
        group_by = [group_by]
    
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Calculate grouped statistics
    grouped = df.groupby(group_by)[numeric_columns].agg([
        'count', 'mean', 'std', 'min', 'max', 'median'
    ])
    
    # Flatten column names
    grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
    
    return {
        'group_by': group_by,
        'numeric_columns': numeric_columns,
        'groups': grouped.reset_index().to_dict(orient='records'),
        'group_count': len(grouped)
    }


def data_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive data profile.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with comprehensive data profile
    """
    # Basic info
    profile = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'memory_usage_bytes': int(df.memory_usage(deep=True).sum()),
        'columns': {}
    }
    
    # Profile each column
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'non_null_count': int(df[col].notna().sum()),
            'null_count': int(df[col].isna().sum()),
            'null_percentage': round(df[col].isna().mean() * 100, 2),
            'unique_count': int(df[col].nunique()),
            'unique_percentage': round(df[col].nunique() / len(df) * 100, 2) if len(df) > 0 else 0
        }
        
        if np.issubdtype(df[col].dtype, np.number):
            col_data = df[col].dropna()
            if len(col_data) > 0:
                col_profile['statistics'] = {
                    'mean': round(float(col_data.mean()), 4),
                    'std': round(float(col_data.std()), 4) if len(col_data) > 1 else 0,
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'q25': float(col_data.quantile(0.25)),
                    'median': float(col_data.median()),
                    'q75': float(col_data.quantile(0.75))
                }
                col_profile['has_negative'] = bool(col_data.min() < 0)
                col_profile['has_zero'] = bool((col_data == 0).any())
        else:
            # Top values for categorical
            top_values = df[col].value_counts().head(5)
            col_profile['top_values'] = {
                str(k): int(v) for k, v in top_values.items()
            }
        
        profile['columns'][col] = col_profile
    
    # Data quality score (simple heuristic)
    null_ratio = df.isna().sum().sum() / (len(df) * len(df.columns)) if len(df) > 0 and len(df.columns) > 0 else 0
    profile['data_quality_score'] = round((1 - null_ratio) * 100, 2)
    
    return profile
