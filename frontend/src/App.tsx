import { useState, useCallback } from 'react'
import Editor from '@monaco-editor/react'
import Plot from 'react-plotly.js'

// API Types
interface QueryResponse {
  success: boolean
  data?: Record<string, unknown>[]
  columns?: string[]
  row_count: number
  mining_result?: MiningResult
  chart?: PlotlyChart
  sql?: string
  error?: string
  query_type?: string
}

interface MiningResult {
  type: string
  method?: string
  n_clusters?: number
  n_anomalies?: number
  inertia?: number
  cluster_sizes?: Record<number, number>
  summary?: Record<string, Record<string, number>>
  [key: string]: unknown
}

interface PlotlyChart {
  data: Plotly.Data[]
  layout: Partial<Plotly.Layout>
}

// Sample queries for quick testing
const SAMPLE_QUERIES = [
  {
    name: 'Basic Select',
    query: 'FROM customers'
  },
  {
    name: 'With Filter',
    query: 'FROM customers WHERE age > 30'
  },
  {
    name: 'K-Means Clustering',
    query: 'FROM customers MINE CLUSTER K=3'
  },
  {
    name: 'Statistics',
    query: 'FROM customers MINE STATISTICS'
  },
  {
    name: 'Anomaly Detection',
    query: 'FROM transactions MINE ANOMALIES'
  },
  {
    name: 'With Visualization',
    query: 'FROM customers DISPLAY AS scatter_plot'
  }
]

function App() {
  const [query, setQuery] = useState<string>(`-- DQML Query Editor
-- Example queries:
-- FROM customers
-- FROM customers WHERE age > 30
-- FROM customers MINE CLUSTER K=3 DISPLAY AS scatter_plot
-- FROM transactions MINE STATISTICS DISPLAY AS heatmap
-- FROM transactions MINE ANOMALIES

FROM customers MINE CLUSTER K=3 DISPLAY AS scatter_plot`)
  
  const [result, setResult] = useState<QueryResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'data' | 'chart' | 'mining'>('data')

  const executeQuery = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      const data: QueryResponse = await response.json()
      
      if (!data.success) {
        setError(data.error || 'Query execution failed')
        setResult(null)
      } else {
        setResult(data)
        // Auto-switch to chart tab if chart is available
        if (data.chart) {
          setActiveTab('chart')
        } else if (data.mining_result) {
          setActiveTab('mining')
        } else {
          setActiveTab('data')
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }, [query])

  const loadSampleQuery = (sampleQuery: string) => {
    setQuery(sampleQuery)
  }

  const clearResults = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div>
          <h1>DQML</h1>
          <span className="header-subtitle">Data Mining Query Language</span>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {SAMPLE_QUERIES.map((sq) => (
            <button
              key={sq.name}
              className="btn btn-secondary"
              onClick={() => loadSampleQuery(sq.query)}
              style={{ padding: '0.5rem 1rem', fontSize: '0.75rem' }}
            >
              {sq.name}
            </button>
          ))}
        </div>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Query Panel */}
        <div className="query-panel">
          <div className="panel-header">
            <span className="panel-title">Query Editor</span>
          </div>
          
          <div className="editor-container">
            <Editor
              height="100%"
              defaultLanguage="sql"
              value={query}
              onChange={(value) => setQuery(value || '')}
              theme="vs-light"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                wordWrap: 'on',
                automaticLayout: true,
              }}
            />
          </div>
          
          <div className="query-actions">
            <button
              className="btn btn-primary"
              onClick={executeQuery}
              disabled={loading || !query.trim()}
            >
              {loading ? 'Executing...' : 'Execute Query'}
            </button>
            <button className="btn btn-secondary" onClick={clearResults}>
              Clear
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="results-panel">
          {/* Tabs */}
          <div className="results-tabs">
            <button
              className={`tab ${activeTab === 'data' ? 'active' : ''}`}
              onClick={() => setActiveTab('data')}
            >
              Data {result?.row_count ? `(${result.row_count})` : ''}
            </button>
            <button
              className={`tab ${activeTab === 'chart' ? 'active' : ''}`}
              onClick={() => setActiveTab('chart')}
              disabled={!result?.chart}
            >
              Chart
            </button>
            <button
              className={`tab ${activeTab === 'mining' ? 'active' : ''}`}
              onClick={() => setActiveTab('mining')}
              disabled={!result?.mining_result}
            >
              Mining Results
            </button>
          </div>

          {/* Results Content */}
          <div className="results-content">
            {error && (
              <div className="empty-state">
                <div className="empty-state-icon">⚠️</div>
                <p style={{ color: '#c62828' }}>{error}</p>
              </div>
            )}

            {!result && !error && (
              <div className="empty-state">
                <div className="empty-state-icon">📊</div>
                <p>Execute a query to see results</p>
              </div>
            )}

            {result && activeTab === 'data' && (
              <DataTable data={result.data || []} columns={result.columns || []} />
            )}

            {result && activeTab === 'chart' && result.chart && (
              <div className="chart-container">
                <Plot
                  data={result.chart.data}
                  layout={{
                    ...result.chart.layout,
                    autosize: true,
                  }}
                  useResizeHandler
                  style={{ width: '100%', height: '100%' }}
                />
              </div>
            )}

            {result && activeTab === 'mining' && result.mining_result && (
              <MiningResults result={result.mining_result} />
            )}
          </div>

          {/* Status Bar */}
          {result && (
            <div className={`status-bar ${loading ? 'loading' : ''}`}>
              {loading ? 'Executing query...' : `Query executed successfully. ${result.row_count} rows returned.`}
              {result.sql && ` SQL: ${result.sql}`}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Data Table Component
function DataTable({ data, columns }: { data: Record<string, unknown>[], columns: string[] }) {
  if (!data.length) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📭</div>
        <p>No data returned</p>
      </div>
    )
  }

  return (
    <div className="data-table-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.slice(0, 100).map((row, i) => (
            <tr key={i}>
              {columns.map((col) => (
                <td key={col}>{formatValue(row[col])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {data.length > 100 && (
        <p style={{ padding: '1rem', color: '#666', textAlign: 'center' }}>
          Showing first 100 of {data.length} rows
        </p>
      )}
    </div>
  )
}

// Mining Results Component
function MiningResults({ result }: { result: MiningResult }) {
  return (
    <div className="mining-results">
      <h3>{result.type?.toUpperCase()} Results</h3>
      
      <div className="mining-stats">
        {result.method && (
          <div className="stat-card">
            <div className="stat-label">Method</div>
            <div className="stat-value">{result.method}</div>
          </div>
        )}
        
        {result.n_clusters !== undefined && (
          <div className="stat-card">
            <div className="stat-label">Clusters</div>
            <div className="stat-value">{result.n_clusters}</div>
          </div>
        )}
        
        {result.n_anomalies !== undefined && (
          <div className="stat-card">
            <div className="stat-label">Anomalies Found</div>
            <div className="stat-value">{result.n_anomalies}</div>
          </div>
        )}
        
        {result.inertia !== undefined && (
          <div className="stat-card">
            <div className="stat-label">Inertia</div>
            <div className="stat-value">{result.inertia.toFixed(2)}</div>
          </div>
        )}
        
        {result.cluster_sizes && (
          <div className="stat-card">
            <div className="stat-label">Cluster Sizes</div>
            <div className="stat-value" style={{ fontSize: '1rem' }}>
              {Object.entries(result.cluster_sizes).map(([k, v]) => (
                <span key={k} style={{ marginRight: '0.5rem' }}>
                  C{k}: {v}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {result.summary && (
        <div style={{ marginTop: '1.5rem' }}>
          <h4>Statistics Summary</h4>
          <table className="data-table" style={{ marginTop: '0.5rem' }}>
            <thead>
              <tr>
                <th>Column</th>
                <th>Mean</th>
                <th>Std</th>
                <th>Min</th>
                <th>Max</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(result.summary).map(([col, stats]) => (
                <tr key={col}>
                  <td>{col}</td>
                  <td>{stats.mean?.toFixed(2)}</td>
                  <td>{stats.std?.toFixed(2)}</td>
                  <td>{stats.min?.toFixed(2)}</td>
                  <td>{stats.max?.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// Helper function to format values
function formatValue(value: unknown): string {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'number') {
    return Number.isInteger(value) ? value.toString() : value.toFixed(4)
  }
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  return String(value)
}

export default App
