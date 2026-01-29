# Contributing to DQML

Thank you for your interest in contributing to DQML! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all skill levels.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- ANTLR4 (for grammar changes)
- Git

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/dqml.git
cd dqml

# Backend setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest black flake8  # Development dependencies

# Frontend setup
cd frontend
npm install
cd ..
```

### Running Tests

```bash
# Run all tests
source venv/bin/activate
PYTHONPATH=backend pytest backend/tests/ -v

# Run with coverage
pytest backend/tests/ --cov=backend/dqml --cov-report=html
```

---

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)

### Suggesting Features

1. Check existing issues/discussions
2. Create a feature request with:
   - Clear description of the feature
   - Use case examples
   - Potential implementation approach

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests and linting:
   ```bash
   pytest backend/tests/ -v
   black backend/
   flake8 backend/
   ```
5. Commit with clear messages:
   ```bash
   git commit -m "[Component] Brief description of change"
   ```
6. Push and create PR:
   ```bash
   git push origin feature/your-feature-name
   ```

---

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for public functions
- Maximum line length: 100 characters

```python
def process_query(query: str, options: Dict[str, Any] = None) -> QueryResult:
    """
    Process a DMQL query and return results.
    
    Args:
        query: The DMQL query string to process
        options: Optional processing options
        
    Returns:
        QueryResult object with execution results
        
    Raises:
        ParseError: If query syntax is invalid
    """
    pass
```

### TypeScript/React

- Use functional components
- Use TypeScript types/interfaces
- Follow React best practices

```typescript
interface QueryResult {
  success: boolean;
  data: Record<string, unknown>[];
  error?: string;
}

const QueryEditor: React.FC<Props> = ({ onExecute }) => {
  // Component implementation
};
```

### Commit Messages

Format: `[Component] Brief description`

Examples:
- `[Parser] Add support for LIMIT clause`
- `[Mining] Implement DBSCAN clustering`
- `[API] Add pagination to results`
- `[Frontend] Add dark mode support`
- `[Docs] Update API documentation`
- `[Tests] Add integration tests for clustering`

---

## Project Structure

### Backend

```
backend/
├── api/           # FastAPI endpoints
├── dqml/
│   ├── parser/    # ANTLR4 grammar and parser
│   ├── executor/  # Query execution
│   ├── mining/    # Data mining algorithms
│   └── visualization/  # Chart generation
└── tests/         # Test files
```

### Frontend

```
frontend/
├── src/
│   ├── components/  # React components
│   ├── hooks/       # Custom hooks
│   └── utils/       # Utility functions
└── public/          # Static assets
```

---

## Adding New Features

### Adding a New Mining Operation

1. **Create the algorithm** in `backend/dqml/mining/`:

```python
# backend/dqml/mining/new_algorithm.py
from dataclasses import dataclass
import pandas as pd

@dataclass
class NewAlgorithmResult:
    data: pd.DataFrame
    metric1: float
    metric2: float

def new_algorithm(df: pd.DataFrame, **params) -> NewAlgorithmResult:
    """Implement new mining algorithm."""
    # Implementation here
    return NewAlgorithmResult(...)
```

2. **Export from `__init__.py`**:

```python
from .new_algorithm import new_algorithm, NewAlgorithmResult
```

3. **Add grammar rule** (if new keyword):

```antlr
miningOperation
    : CLUSTER (K '=' INT)?
    | STATISTICS
    | ANOMALIES
    | NEW_ALGORITHM  // Add new operation
    ;
```

4. **Regenerate parser**:

```bash
cd backend/dqml/parser
antlr4 -Dlanguage=Python3 -visitor DMQL.g4
```

5. **Update API** in `backend/api/main.py`

6. **Add tests**

### Adding a New Chart Type

1. **Add function** in `backend/dqml/visualization/charts.py`:

```python
def generate_new_chart(df: pd.DataFrame, **kwargs) -> ChartResult:
    """Generate new chart type."""
    fig = go.Figure(data=[...])
    return ChartResult(figure=fig, chart_type='new_chart')
```

2. **Register in factory** (if using factory pattern)

3. **Add frontend support** if needed

---

## Testing Guidelines

### Writing Tests

- One test file per module
- Use descriptive test names
- Use fixtures for common setup
- Test both success and error cases

```python
class TestNewFeature:
    """Tests for new feature."""
    
    def test_basic_functionality(self, sample_data):
        """Test basic functionality works."""
        result = new_feature(sample_data)
        assert result.success
        
    def test_handles_empty_input(self):
        """Test graceful handling of empty input."""
        result = new_feature(pd.DataFrame())
        assert result.success
        assert len(result.data) == 0
        
    def test_raises_on_invalid_input(self):
        """Test appropriate error on invalid input."""
        with pytest.raises(ValueError):
            new_feature(None)
```

### Test Coverage

Aim for at least 80% code coverage on new code.

---

## Documentation

### Code Documentation

- Add docstrings to all public functions
- Update README if adding major features
- Update API docs for endpoint changes
- Add examples for new functionality

### Generating Documentation

```bash
# Build API docs (if using Sphinx)
cd docs
make html
```

---

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release PR
4. After merge, create Git tag
5. GitHub Actions will build and publish

---

## Getting Help

- Open an issue for bugs/questions
- Check existing documentation
- Join discussions on GitHub

---

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- Project README (for major contributions)

Thank you for contributing to DQML! 🎉
