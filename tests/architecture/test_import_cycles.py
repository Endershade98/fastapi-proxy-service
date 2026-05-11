# tests/architecture/test_import_cycles.py

from pathlib import Path


def test_application_should_not_be_imported_by_domain():
    domain_files = Path("app/domain").rglob("*.py")

    for file in domain_files:
        content = file.read_text()

        assert "app.application" not in content