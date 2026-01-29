"""
Tests for DQML Visualization Module

Tests chart generation functions using Plotly.
"""

import pytest
import pandas as pd
import numpy as np
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from dqml.visualization import (
    ChartResult,
    generate_chart,
    generate_cluster_visualization,
    generate_anomaly_visualization,
    auto_visualize
)


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B'],
        'value': [10, 20, 15, 25, 30, 12, 18, 22],
        'score': [1.5, 2.3, 1.8, 2.1, 2.8, 1.2, 1.9, 2.5]
    })


@pytest.fixture
def numeric_df():
    """Create numeric-only DataFrame."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50),
        'z': np.random.randn(50)
    })


@pytest.fixture
def clustered_df():
    """Create DataFrame with cluster labels."""
    np.random.seed(42)
    n = 30
    return pd.DataFrame({
        'feature1': np.concatenate([np.random.randn(10) + i for i in range(3)]),
        'feature2': np.concatenate([np.random.randn(10) + i for i in range(3)]),
        'cluster': [0]*10 + [1]*10 + [2]*10
    })


@pytest.fixture
def anomaly_df():
    """Create DataFrame with anomaly labels."""
    np.random.seed(42)
    n = 50
    df = pd.DataFrame({
        'feature1': np.random.randn(n),
        'feature2': np.random.randn(n),
        'anomaly_score': np.random.rand(n)
    })
    df['is_anomaly'] = df['anomaly_score'] > 0.8
    return df


class TestChartResult:
    """Tests for ChartResult class."""
    
    def test_chart_result_creation(self, sample_df):
        """Test ChartResult is created properly."""
        result = generate_chart(sample_df, 'bar_chart')
        
        assert isinstance(result, ChartResult)
        assert result.chart_type == 'bar_chart'
        assert result.figure is not None
    
    def test_to_json(self, sample_df):
        """Test conversion to JSON."""
        result = generate_chart(sample_df, 'bar_chart')
        json_str = result.to_json()
        
        assert isinstance(json_str, str)
        # Should be valid JSON
        parsed = json.loads(json_str)
        assert 'data' in parsed
        assert 'layout' in parsed
    
    def test_to_dict(self, sample_df):
        """Test conversion to dictionary."""
        result = generate_chart(sample_df, 'bar_chart')
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'data' in result_dict
        assert 'layout' in result_dict
    
    def test_to_html(self, sample_df):
        """Test conversion to HTML."""
        result = generate_chart(sample_df, 'bar_chart')
        html = result.to_html()
        
        assert isinstance(html, str)
        assert '<div' in html or 'plotly' in html.lower()


class TestBarChart:
    """Tests for bar chart generation."""
    
    def test_bar_chart_basic(self, sample_df):
        """Test basic bar chart generation."""
        result = generate_chart(sample_df, 'bar_chart', x_col='category', y_col='value')
        
        assert result.chart_type == 'bar_chart'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'bar'
    
    def test_bar_chart_auto_columns(self, sample_df):
        """Test bar chart with auto-detected columns."""
        result = generate_chart(sample_df, 'bar_chart')
        
        assert result.chart_type == 'bar_chart'
    
    def test_bar_alias(self, sample_df):
        """Test 'bar' alias for bar_chart."""
        result = generate_chart(sample_df, 'bar', x_col='category', y_col='value')
        
        assert result.chart_type == 'bar'


class TestScatterPlot:
    """Tests for scatter plot generation."""
    
    def test_scatter_basic(self, numeric_df):
        """Test basic scatter plot."""
        result = generate_chart(numeric_df, 'scatter_plot', x_col='x', y_col='y')
        
        assert result.chart_type == 'scatter_plot'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'scatter'
    
    def test_scatter_with_color(self, clustered_df):
        """Test scatter plot with color encoding."""
        result = generate_chart(
            clustered_df, 'scatter_plot',
            x_col='feature1', y_col='feature2', color_col='cluster'
        )
        
        assert result.chart_type == 'scatter_plot'
    
    def test_scatter_auto_columns(self, numeric_df):
        """Test scatter plot with auto-detected columns."""
        result = generate_chart(numeric_df, 'scatter_plot')
        
        assert result.chart_type == 'scatter_plot'


class TestLineChart:
    """Tests for line chart generation."""
    
    def test_line_chart_basic(self):
        """Test basic line chart."""
        df = pd.DataFrame({
            'time': range(10),
            'value': [1, 3, 2, 4, 3, 5, 4, 6, 5, 7]
        })
        
        result = generate_chart(df, 'line_chart', x_col='time', y_col='value')
        
        assert result.chart_type == 'line_chart'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'scatter'
        assert fig_dict['data'][0]['mode'] == 'lines'


class TestHeatmap:
    """Tests for heatmap generation."""
    
    def test_heatmap_correlation(self, numeric_df):
        """Test correlation heatmap."""
        result = generate_chart(numeric_df, 'heatmap')
        
        assert result.chart_type == 'heatmap'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'heatmap'


class TestHistogram:
    """Tests for histogram generation."""
    
    def test_histogram_basic(self, numeric_df):
        """Test basic histogram."""
        result = generate_chart(numeric_df, 'histogram', x_col='x')
        
        assert result.chart_type == 'histogram'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'histogram'


class TestBoxPlot:
    """Tests for box plot generation."""
    
    def test_box_plot_basic(self, sample_df):
        """Test basic box plot."""
        result = generate_chart(sample_df, 'box_plot', y_col='value')
        
        assert result.chart_type == 'box_plot'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'box'
    
    def test_box_plot_grouped(self, sample_df):
        """Test grouped box plot."""
        result = generate_chart(sample_df, 'box_plot', x_col='category', y_col='value')
        
        assert result.chart_type == 'box_plot'


class TestPieChart:
    """Tests for pie chart generation."""
    
    def test_pie_chart_basic(self, sample_df):
        """Test basic pie chart."""
        result = generate_chart(sample_df, 'pie_chart', x_col='category', y_col='value')
        
        assert result.chart_type == 'pie_chart'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'pie'


class TestTable:
    """Tests for table visualization."""
    
    def test_table_basic(self, sample_df):
        """Test table visualization."""
        result = generate_chart(sample_df, 'table')
        
        assert result.chart_type == 'table'
        fig_dict = result.to_dict()
        assert fig_dict['data'][0]['type'] == 'table'
    
    def test_table_max_rows(self):
        """Test table with max rows limit."""
        df = pd.DataFrame({'x': range(200)})
        result = generate_chart(df, 'table', max_rows=50)
        
        assert result.chart_type == 'table'


class TestSpecializedCharts:
    """Tests for specialized chart functions."""
    
    def test_cluster_visualization_2d(self, clustered_df):
        """Test 2D cluster visualization."""
        result = generate_cluster_visualization(
            clustered_df,
            feature_cols=['feature1', 'feature2'],
            cluster_col='cluster'
        )
        
        assert isinstance(result, ChartResult)
        assert result.chart_type == 'cluster_scatter'
    
    def test_cluster_visualization_3d(self):
        """Test 3D cluster visualization."""
        np.random.seed(42)
        df = pd.DataFrame({
            'f1': np.random.randn(30),
            'f2': np.random.randn(30),
            'f3': np.random.randn(30),
            'cluster': [0]*10 + [1]*10 + [2]*10
        })
        
        result = generate_cluster_visualization(
            df,
            feature_cols=['f1', 'f2', 'f3'],
            cluster_col='cluster'
        )
        
        assert isinstance(result, ChartResult)
    
    def test_anomaly_visualization(self, anomaly_df):
        """Test anomaly visualization."""
        result = generate_anomaly_visualization(
            anomaly_df,
            feature_cols=['feature1', 'feature2'],
            anomaly_col='is_anomaly',
            score_col='anomaly_score'
        )
        
        assert isinstance(result, ChartResult)
        assert result.chart_type == 'anomaly_visualization'


class TestAutoVisualize:
    """Tests for auto_visualize function."""
    
    def test_auto_visualize_small_data(self):
        """Test auto visualization for small dataset (should be table)."""
        df = pd.DataFrame({'x': range(10), 'y': range(10)})
        result = auto_visualize(df)
        
        assert result.chart_type == 'table'
    
    def test_auto_visualize_clustered(self, clustered_df):
        """Test auto visualization for clustered data."""
        # Rename to match expectation
        df = clustered_df.copy()
        result = auto_visualize(df)
        
        assert result.chart_type == 'scatter_plot'
    
    def test_auto_visualize_numeric(self):
        """Test auto visualization for numeric-only data."""
        np.random.seed(42)
        df = pd.DataFrame({
            'a': np.random.randn(50),
            'b': np.random.randn(50),
            'c': np.random.randn(50)
        })
        result = auto_visualize(df)
        
        # Should be heatmap for numeric data
        assert result.chart_type in ['heatmap', 'scatter_plot']
    
    def test_auto_visualize_anomaly(self, anomaly_df):
        """Test auto visualization for anomaly data."""
        result = auto_visualize(anomaly_df)
        
        assert result.chart_type == 'anomaly_visualization'


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_unknown_chart_type_defaults_to_table(self, sample_df):
        """Test that unknown chart type defaults to table."""
        result = generate_chart(sample_df, 'unknown_type')
        
        assert result.chart_type == 'table'
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame()
        result = generate_chart(df, 'table')
        
        assert result.chart_type == 'table'
    
    def test_chart_with_title(self, sample_df):
        """Test chart with custom title."""
        title = "My Custom Chart"
        result = generate_chart(sample_df, 'bar_chart', title=title)
        
        fig_dict = result.to_dict()
        assert fig_dict['layout']['title']['text'] == title
