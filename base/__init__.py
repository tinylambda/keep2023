import logging
import sys

keep_logger = logging.getLogger("KeepLogger")
keep_logger.setLevel(logging.INFO)

logger_handler_stderr = logging.StreamHandler(stream=sys.stderr)
logger_formatter = logging.Formatter(
    fmt="{asctime}\t{levelname}\t{message!r}", style="{"
)
logger_handler_stderr.setFormatter(logger_formatter)
keep_logger.addHandler(logger_handler_stderr)
