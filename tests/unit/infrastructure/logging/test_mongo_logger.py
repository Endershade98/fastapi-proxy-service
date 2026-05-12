# tests/unit/infrastructure/logging/test_mongo_logger.py

from app.infrastructure.app_logging.mongo_logger import MongoLogger


class FakeCollection:
    def __init__(self):
        self.inserted = []

    def insert_one(self, doc):
        self.inserted.append(doc)
        return True


def test_mongo_logger_logs_event():
    collection = FakeCollection()
    logger = MongoLogger(collection)

    logger.log_event({"message": "hello"})

    assert len(collection.inserted) == 1
    assert collection.inserted[0]["message"] == "hello"