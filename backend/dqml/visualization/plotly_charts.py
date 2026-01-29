"""
Plotly Chart Generation for DMQL Visualization

This module provides chart generation capabilities for DMQL queries
using Plotly for interactive visualizations.

Usage:
    from backend.dqml.visualization import generate_chart
    
    df = pd.DataFrame(...)
    chart_json = generate_chart(df, 'scatter_plot', x_col='age', y_col='income')
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json


class ChartResult:
    """Result of chart generation."""
    
    def __init__(
        self,
        figure: go.Figure,
        chart_type: str,
        config: Dict[str, Any] = None
    ):
        self.figure = figure
        self.chart_type = chart_type
        self.config = config or {}
    
    def to_json(self) -> str:
        """Convert figure to JSON string."""
        return self.figure.to_json()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert figure to dictionary."""
        return json.loads(self.figure.to_json())
    
    def to_html(self, full_html: bool = False) -> str:
        """Convert figure to HTML string."""
        return self.figure.to_html(full_html=full_html)
    
    def show(self):
        """Display the figure (in notebook or browser)."""
        self.figure.show()


def generate_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> ChartResult:
    """
    Generate a Plotly chart from a DataFrame.
    
    Args:
        df: Input DataFrame
        chart_type: Type of chart ('bar_chart', 'scatter_plot', 'line_chart', 
                    'heatmap', 'histogram', 'box_plot', 'pie_chart', 'table')
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Column for color encoding
        title: Chart title
        **kwargs: Additional chart-specific arguments
        
    Returns:
        ChartResult containing the Plotly figure
    """
    # Normalize chart type
    chart_type = chart_type.lower().replace('-', '_')
    
    # Map to generation function
    chart_functions = {
        'bar_chart': _generate_bar_chart,
        'bar': _generate_bar_chart,
        'scatter_plot': _generate_scatter_plot,
        'scatter': _generate_scatter_plot,
        'line_chart': _generate_line_chart,
        'line': _generate_line_chart,
        'heatmap': _generate_heatmap,
        'histogram': _generate_histogram,
        'box_plot': _generate_box_plot,
        'box': _generate_box_plot,
        'pie_chart': _generate_pie_chart,
        'pie': _generate_pie_chart,
        'table': _generate_table,
    }
    
    if chart_type not in chart_functions:
        # Default to table if chart type not recognized
        chart_type = 'table'
    
    # Generate the chart
    fig = chart_functions[chart_type](
        df, x_col=x_col, y_col=y_col, color_col=color_col, 
        title=title, **kwargs
    )
    
    # Apply common styling
    fig = _apply_common_styling(fig, title)
    
    return ChartResult(figure=fig, chart_type=chart_type)


def _generate_bar_chart(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    orientation: str = 'v',
    **kwargs
) -> go.Figure:
    """Generate a bar chart."""
    # Auto-detect columns if not specified
    if x_col is None:
        # Use first categorical column for x
        cat_cols = df.select_dtypes(exclude=[np.number]).columns
        x_col = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
    
    if y_col is None:
        # Use first numeric column for y
        num_cols = df.select_dtypes(include=[np.number]).columns
        y_col = num_cols[0] if len(num_cols) > 0 else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    fig = px.bar(
        df, x=x_col, y=y_col, color=color_col,
        title=title or f'{y_col} by {x_col}',
        orientation=orientation
    )
    
    return fig


def _generate_scatter_plot(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    size_col: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Generate a scatter plot."""
    # Auto-detect numeric columns
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if x_col is None and len(num_cols) >= 1:
        x_col = num_cols[0]
    if y_col is None and len(num_cols) >= 2:
        y_col = num_cols[1]
    
    if x_col is None or y_col is None:
        raise ValueError("Need at least 2 numeric columns for scatter plot")
    
    # Check if this is clustered data
    if 'cluster' in df.columns and color_col is None:
        color_col = 'cluster'
    
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col,
        size=size_col,
        title=title or f'{y_col} vs {x_col}'
    )
    
    return fig


def _generate_line_chart(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Generate a line chart."""
    # Auto-detect columns
    if x_col is None:
        # Try to find a date/time column or index
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            x_col = date_cols[0]
        else:
            x_col = df.columns[0]
    
    if y_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        y_col = num_cols[0] if num_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    fig = px.line(
        df, x=x_col, y=y_col, color=color_col,
        title=title or f'{y_col} over {x_col}'
    )
    
    return fig


def _generate_heatmap(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Generate a heatmap."""
    # If correlation matrix needed
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if x_col is None and y_col is None:
        # Generate correlation matrix heatmap
        corr_matrix = df[num_cols].corr() if num_cols else df.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect='auto',
            color_continuous_scale='RdBu_r',
            title=title or 'Correlation Heatmap'
        )
    else:
        # 2D density heatmap
        fig = px.density_heatmap(
            df, x=x_col, y=y_col,
            title=title or f'Density: {y_col} vs {x_col}'
        )
    
    return fig


def _generate_histogram(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    nbins: int = 30,
    **kwargs
) -> go.Figure:
    """Generate a histogram."""
    if x_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        x_col = num_cols[0] if num_cols else df.columns[0]
    
    fig = px.histogram(
        df, x=x_col, color=color_col,
        nbins=nbins,
        title=title or f'Distribution of {x_col}'
    )
    
    return fig


def _generate_box_plot(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Generate a box plot."""
    if y_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        y_col = num_cols[0] if num_cols else df.columns[0]
    
    if x_col is None:
        cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
        x_col = cat_cols[0] if cat_cols else None
    
    fig = px.box(
        df, x=x_col, y=y_col, color=color_col,
        title=title or f'Distribution of {y_col}'
    )
    
    return fig


def _generate_pie_chart(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Generate a pie chart."""
    # x_col is names, y_col is values
    if x_col is None:
        cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
        x_col = cat_cols[0] if cat_cols else df.columns[0]
    
    if y_col is None:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        y_col = num_cols[0] if num_cols else 'count'
    
    # Aggregate if needed
    if y_col == 'count':
        agg_df = df[x_col].value_counts().reset_index()
        agg_df.columns = [x_col, 'count']
        y_col = 'count'
    else:
        agg_df = df.groupby(x_col)[y_col].sum().reset_index()
    
    fig = px.pie(
        agg_df, names=x_col, values=y_col,
        title=title or f'Distribution of {x_col}'
    )
    
    return fig


def _generate_table(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None,
    max_rows: int = 100,
    **kwargs
) -> go.Figure:
    """Generate a table visualization."""
    # Limit rows for display
    display_df = df.head(max_rows)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(display_df.columns),
            fill_color='paleturquoise',
            align='left',
            font=dict(size=12)
        ),
        cells=dict(
            values=[display_df[col] for col in display_df.columns],
            fill_color='lavender',
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title=title or 'Data Table',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


def _apply_common_styling(fig: go.Figure, title: Optional[str] = None) -> go.Figure:
    """Apply common styling to all charts."""
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=40, r=40, t=60 if title else 40, b=40),
        font=dict(family='Arial, sans-serif', size=12),
        showlegend=True
    )
    
    return fig


# ============================================================================
# SPECIALIZED CHART FUNCTIONS
# ============================================================================

def generate_cluster_visualization(
    df: pd.DataFrame,
    feature_cols: List[str],
    cluster_col: str = 'cluster',
    title: str = 'Cluster Visualization'
) -> ChartResult:
    """
    Generate visualization for clustered data.
    
    Uses 2D or 3D scatter plot depending on number of features.
    """
    if len(feature_cols) >= 3:
        # 3D scatter
        fig = px.scatter_3d(
            df,
            x=feature_cols[0],
            y=feature_cols[1],
            z=feature_cols[2],
            color=cluster_col,
            title=title
        )
    else:
        # 2D scatter
        fig = px.scatter(
            df,
            x=feature_cols[0],
            y=feature_cols[1] if len(feature_cols) > 1 else feature_cols[0],
            color=cluster_col,
            title=title
        )
    
    return ChartResult(figure=fig, chart_type='cluster_scatter')


def generate_anomaly_visualization(
    df: pd.DataFrame,
    feature_cols: List[str],
    anomaly_col: str = 'is_anomaly',
    score_col: str = 'anomaly_score',
    title: str = 'Anomaly Detection Results'
) -> ChartResult:
    """
    Generate visualization for anomaly detection results.
    """
    # Create subplot with scatter and histogram
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Data Points (Anomalies Highlighted)', 'Anomaly Score Distribution'],
        row_heights=[0.7, 0.3]
    )
    
    # Scatter plot
    colors = df[anomaly_col].map({True: 'red', False: 'blue'})
    
    fig.add_trace(
        go.Scatter(
            x=df[feature_cols[0]],
            y=df[feature_cols[1]] if len(feature_cols) > 1 else df[feature_cols[0]],
            mode='markers',
            marker=dict(
                color=colors,
                size=8,
                opacity=0.7
            ),
            name='Data Points'
        ),
        row=1, col=1
    )
    
    # Score histogram
    if score_col in df.columns:
        fig.add_trace(
            go.Histogram(
                x=df[score_col],
                nbinsx=30,
                name='Anomaly Scores'
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        title=title,
        showlegend=True,
        height=600
    )
    
    return ChartResult(figure=fig, chart_type='anomaly_visualization')


def generate_statistics_dashboard(
    stats_result: Dict[str, Any],
    title: str = 'Statistics Dashboard'
) -> ChartResult:
    """
    Generate a dashboard for statistics results.
    """
    summary = stats_result.get('summary', {})
    
    if not summary:
        # Empty figure
        fig = go.Figure()
        fig.add_annotation(text="No statistics to display", showarrow=False)
        return ChartResult(figure=fig, chart_type='stats_dashboard')
    
    cols = list(summary.keys())
    n_cols = len(cols)
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=n_cols,
        subplot_titles=cols
    )
    
    # Add box plots for each numeric column
    for i, col in enumerate(cols, 1):
        col_stats = summary[col]
        
        # Create synthetic box plot data
        fig.add_trace(
            go.Box(
                y=[col_stats['min'], col_stats['q25'], col_stats['median'], 
                   col_stats['q75'], col_stats['max']],
                name=col,
                boxpoints=False
            ),
            row=1, col=i
        )
    
    fig.update_layout(
        title=title,
        showlegend=False,
        height=400
    )
    
    return ChartResult(figure=fig, chart_type='stats_dashboard')


def auto_visualize(
    df: pd.DataFrame,
    title: Optional[str] = None
) -> ChartResult:
    """
    Automatically choose the best visualization for the data.
    
    Uses heuristics based on column types and data characteristics.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Check for cluster column
    if 'cluster' in df.columns:
        if len(num_cols) >= 2:
            return generate_chart(df, 'scatter_plot', 
                                  x_col=num_cols[0], y_col=num_cols[1],
                                  color_col='cluster', title=title)
    
    # Check for anomaly column
    if 'is_anomaly' in df.columns:
        if len(num_cols) >= 2:
            return generate_anomaly_visualization(df, num_cols[:2], title=title or 'Anomaly Results')
    
    # Small dataset: table
    if len(df) <= 20:
        return generate_chart(df, 'table', title=title)
    
    # Only numeric columns: correlation heatmap or scatter
    if len(num_cols) >= 2 and len(cat_cols) == 0:
        if len(num_cols) <= 10:
            return generate_chart(df, 'heatmap', title=title or 'Correlation Heatmap')
        else:
            return generate_chart(df, 'scatter_plot', 
                                  x_col=num_cols[0], y_col=num_cols[1],
                                  title=title)
    
    # Mix of numeric and categorical
    if len(num_cols) >= 1 and len(cat_cols) >= 1:
        # Bar chart with categorical x, numeric y
        return generate_chart(df, 'bar_chart',
                              x_col=cat_cols[0], y_col=num_cols[0],
                              title=title)
    
    # Default: table
    return generate_chart(df, 'table', title=title)
