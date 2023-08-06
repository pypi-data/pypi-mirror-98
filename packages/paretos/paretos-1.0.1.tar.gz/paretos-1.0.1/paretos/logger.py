import json
import logging
import sys


class DefaultLogger(logging.LoggerAdapter):
    def __init__(self, level: int = logging.INFO):
        logger = logging.getLogger("paretos")
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        log_format = "[%(asctime)s] %(name)s.%(levelname)s: %(message)s"
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        super().__init__(logger, {})

    def process(self, msg, kwargs):
        data = {}

        if "extra" in kwargs:
            data = kwargs["extra"]

        # ensure single line log
        msg = msg.replace("\r", "\\r").replace("\n", "\\n")

        msg += " " + json.dumps(data)

        return msg, kwargs
