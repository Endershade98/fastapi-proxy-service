# tests/architecture/test_domain_rules.py

from pathlib import Path


ROOT = Path("app/domain")


FORBIDDEN = [
    "fastapi",
    "sqlalchemy",
    "redis",
    "motor",
    "httpx",
    "celery",
    "app.infrastructure",
    "app.interfaces",
    "app.application",
]


def test_domain_must_be_pure():
    for file in ROOT.rglob("*.py"):
        content = file.read_text()

        for bad in FORBIDDEN:
            assert bad not in content, f"{file} imports forbidden dependency: {bad}"