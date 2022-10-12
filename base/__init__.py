import logging
import sys

keep_logger = logging.getLogger("KeepLogger")
keep_logger.setLevel(logging.INFO)

logger_handler_stderr = logging.StreamHandler(stream=sys.stderr)
keep_logger.addHandler(logger_handler_stderr)
