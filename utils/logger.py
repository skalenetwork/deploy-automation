import sys
import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler


LOG_FILE_SIZE_MB = 100
LOG_FILE_SIZE_BYTES = LOG_FILE_SIZE_MB * 1000000
LOG_FORMAT = '[%(asctime)s %(levelname)s] %(name)s - %(threadName)s - %(message)s'
CLI_LOG_FORMAT = '[%(asctime)s %(levelname)s] %(message)s'
LOG_BACKUP_COUNT = 3
LOG_FILE_PATH = './cli.log'


def init_logger(log_file_path, enable_stream_handler=False):
    handlers = []

    formatter = Formatter(LOG_FORMAT)
    cli_formatter = Formatter(CLI_LOG_FORMAT)
    f_handler = RotatingFileHandler(log_file_path, maxBytes=LOG_FILE_SIZE_BYTES,
                                    backupCount=LOG_BACKUP_COUNT)

    f_handler.setFormatter(formatter)
    f_handler.setLevel(logging.DEBUG)
    handlers.append(f_handler)

    if enable_stream_handler:
        stream_handler = StreamHandler(sys.stderr)
        stream_handler.setFormatter(cli_formatter)
        stream_handler.setLevel(logging.INFO)
        handlers.append(stream_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)
