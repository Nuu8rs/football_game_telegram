import logging
from colorlog import ColoredFormatter

class LoggerConfig:
    @staticmethod
    def setup_logger():
        log_format = '%(asctime)s | %(levelname)-5s | %(filename)-14s | %(funcName)-10s | %(message)s'
        color_format = (
            '%(log_color)s%(asctime)s | %(levelname)-5s | %(filename)-14s | %(funcName)-10s | %(message)s%(reset)s'
        )

        formatter = ColoredFormatter(
            fmt=color_format,
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        # Общий обработчик
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # Общая настройка
        logging.basicConfig(level=logging.DEBUG, handlers=[handler], force=True)

        # Логгер SQLAlchemy
        sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
        sqlalchemy_logger.setLevel(logging.WARNING)  # Уровень WARNING
        sqlalchemy_handler = logging.StreamHandler()
        sqlalchemy_handler.setFormatter(formatter)
        sqlalchemy_logger.handlers.clear()
        sqlalchemy_logger.addHandler(sqlalchemy_handler)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
    
LoggerConfig.setup_logger()
logger = LoggerConfig.get_logger(__name__)