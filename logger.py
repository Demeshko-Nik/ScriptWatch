import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(log_directory="logs", log_file="app.log", backup_count=7):
    """
    Настройка логгера с ежедневной ротацией файлов и добавлением даты в имя файла.

    :param log_directory: Директория для хранения логов.
    :param log_file: Имя файла лога (без даты).
    :param backup_count: Количество дней для хранения логов.
    :return: Настроенный логгер.
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Добавляем дату в имя файла
    log_file_with_date = f"{datetime.now().strftime('%Y-%m-%d')}_{log_file}"

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    # Создаем обработчик с ротацией по дням
    handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, log_file_with_date),
        when="midnight",
        interval=1,
        backupCount=backup_count,
    )
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(handler)
    return logger