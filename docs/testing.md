# Tutti i test
pytest

# Solo unit
pytest -m unit

# Solo integration
pytest -m integration

# Solo e2e
pytest -m e2e

# Coverage
pytest --cov=app --cov-report=term-missing

# Test specifico
pytest tests/unit/domain/test_cache_entry.py

# Verbose
pytest -v