import logging

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.origin = f"{record.filename}:{record.lineno}"
    return record


def setup_logging(level=logging.INFO, filename: str = None):
    logging.setLogRecordFactory(record_factory)
    logging_fmt = "%(asctime)s - %(origin)-30s - %(levelname)s - %(message)s"
    logging.basicConfig(format=logging_fmt, level=level, filename=filename)
