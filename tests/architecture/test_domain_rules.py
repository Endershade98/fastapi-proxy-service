# tests/architecture/test_domain_rules.py

from pathlib import Path


DOMAIN_PATH = Path("app/domain")


FORBIDDEN_IMPORTS = [
    "fastapi",
    "sqlalchemy",
    "redis",
    "pymongo",
    "requests",
    "httpx",
    "celery",
]


def test_domain_must_not_depend_on_frameworks():
    py_files = DOMAIN_PATH.rglob("*.py")

    for file in py_files:
        content = file.read_text(encoding="utf-8")

        for forbidden in FORBIDDEN_IMPORTS:
            assert forbidden not in content, (
                f"{file} imports forbidden dependency {forbidden}"
            )