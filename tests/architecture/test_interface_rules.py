# tests/architecture/test_interface_rules.py

from pathlib import Path


ROOT = Path("app/interfaces")


def test_interfaces_should_use_application():
    for file in ROOT.rglob("*.py"):
        content = file.read_text()

        assert "app.infrastructure" not in content, \
            f"{file} should not depend directly on infrastructure"