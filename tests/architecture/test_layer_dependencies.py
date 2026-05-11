# tests/architecture/test_layer_dependencies.py

from pathlib import Path


def test_domain_must_not_import_outer_layers():
    domain_files = Path("app/domain").rglob("*.py")

    forbidden = [
        "app.infrastructure",
        "app.interfaces",
        "app.application",
    ]

    for file in domain_files:
        content = file.read_text(encoding="utf-8")

        for item in forbidden:
            assert item not in content, (
                f"{file} imports outer layer {item}"
            )