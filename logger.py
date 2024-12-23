import logging
import os
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class Logger:

    FMT = f"[%(levelname)s] %(asctime)s : %(module)s : %(funcName)s : %(lineno)d :: -  %(message)s"
    DATE_FMT = '%Y-%m-%d %H:%M:%S'

    class CustomFormatter(logging.Formatter):
        grey = '\x1b[38;21m'
        blue = '\x1b[38;5;39m'
        yellow = '\x1b[38;5;226m'
        red = '\x1b[38;5;196m'
        bold_red = '\x1b[31;1m'
        reset = '\x1b[0m'
        green = '\x1b[38;5;46m'
        bold_green = '\x1b[32;1m'

        def __init__(self, fmt, datefmt):
            super().__init__()
            self.fmt = fmt
            self.datefmt = datefmt
            self.FORMATS = {
                logging.DEBUG: self.bold_green + self.fmt + self.reset,
                logging.INFO: self.blue + self.fmt + self.reset,
                logging.WARNING: self.yellow + self.fmt + self.reset,
                logging.ERROR: self.red + self.fmt + self.reset,
                logging.CRITICAL: self.bold_red + self.fmt + self.reset
            }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
            return formatter.format(record)

    LOG_FOLDER = f"{os.getcwd()}/log"
    DEFAULT_FILE_NAME = "rag_trading.log"
    LOG_FILE = f"{LOG_FOLDER}/{DEFAULT_FILE_NAME}"
    LOG_FILE_SIZE = 2097152
    BACKUP_COUNT = 10
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    try:
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
    except OSError:
        print(f" 폴더 생성하다 에러남 {LOG_FOLDER}")

    FORMATTER = logging.Formatter(fmt=FMT)

    HANDLER = RotatingFileHandler(
        encoding='utf-8',
        filename=LOG_FILE,
        maxBytes=LOG_FILE_SIZE,
        backupCount=BACKUP_COUNT
    )
    HANDLER.setLevel(logging.DEBUG)
    HANDLER.setFormatter(FORMATTER)

    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setLevel(logging.DEBUG)
    STREAM_HANDLER.setFormatter(CustomFormatter(FMT, DATE_FMT))
    REGISTERED_LOGGER = {}

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        if name in cls.REGISTERED_LOGGER:
            return logger

        logger.addHandler(cls.STREAM_HANDLER)
        logger.addHandler(cls.HANDLER)
        logger.setLevel(logging.DEBUG)
        cls.REGISTERED_LOGGER[name] = logger
        return logger

    @classmethod
    def set_stream_level(cls, level):
        """스트림 핸들러의 레벨을 설정
        CRITICAL  50
        ERROR     40
        WARNING   30
        INFO      20
        DEBUG     10
        NOTSET    0
        """
        cls.STREAM_HANDLER.setLevel(level)

    @classmethod
    def change_log_file(cls, log_file=DEFAULT_FILE_NAME):
        """파일 핸들러의 로그 파일을 변경"""
        cls.LOG_FILE = f"{cls.LOG_FOLDER}/{log_file}"
        new_file_handler = RotatingFileHandler(
            filename=cls.LOG_FILE,
            maxBytes=cls.LOG_FILE_SIZE,
            backupCount=cls.BACKUP_COUNT,
        )
        new_file_handler.setLevel(logging.DEBUG)
        new_file_handler.setFormatter(cls.FORMATTER)

        for logger in cls.REGISTERED_LOGGER.values():
            logger.removeHandler(cls.HANDLER)
            logger.addHandler(new_file_handler)
            cls.HANDLER.close()

        cls.HANDLER = new_file_handler

class SafeRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(
            self,
            filename,
            where='h',
            interval=1,
            backup_count=0,
            encoding=None,
            delay=False,
            utc=False,
    ):
        TimedRotatingFileHandler.__init__(
            self,
            filename,
            where,
            interval,
            backup_count,
            encoding,
            delay,
            utc
        )

    def do_rollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(t + addend)
        dfn = self.baseFilename + "," + time.strftime(self.suffix, time_tuple)

        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.rename(s)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if self.when == "MIDNIGHT" or self.when.startswith("`") and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:
                    addend = -3600
                else:
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at