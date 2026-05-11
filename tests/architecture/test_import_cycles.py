# tests/architecture/test_import_cycles.py

import pkgutil
import importlib


SKIP_MODULES = [
    "app.infrastructure.db.postgres",
    "app.infrastructure.celery.celery_app",
]


def test_all_modules_importable():
    for module in pkgutil.walk_packages(["app"], prefix="app."):

        if module.name in SKIP_MODULES:
            continue

        importlib.import_module(module.name)