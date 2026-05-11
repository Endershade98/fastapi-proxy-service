# tests/architecture/test_layer_dependencies.py

from pathlib import Path


def test_bootstrap_can_use_everything():
    file = Path("app/bootstrap/container.py")

    content = file.read_text()

    assert "app.domain" in content
    assert "app.application" in content
    assert "app.infrastructure" in content