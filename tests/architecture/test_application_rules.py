# tests/architecture/test_application_rules.py

from pathlib import Path


ROOT = Path("app/application")

FORBIDDEN = [
    "fastapi",
    "sqlalchemy",
    "redis",
    "motor",
    "celery",
    "app.infrastructure",
    "app.interfaces",
]


def test_application_must_not_depend_on_outer_layers():
    for file in ROOT.rglob("*.py"):
        content = file.read_text()

        for bad in FORBIDDEN:
            assert bad not in content, f"{file} imports forbidden dependency: {bad}"