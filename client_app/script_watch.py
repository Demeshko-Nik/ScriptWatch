import time
import traceback
import psutil
import tracemalloc
import requests
from logger import setup_logger

log = setup_logger(log_directory='logs',log_file='scriptwatch.log')

def monitor_script(script_name, start_func):
    """
    Основная функция сбора информации о выполнении скриптов

    :param script_name: Имя запускаемого скрипта.
    :param start_func: Функция запуска скрипта.
    """

    start_time = time.time()
    process = psutil.Process()
    metrics = {
        'script_name' : script_name, #Имя скрипта
        'exec_status': 'unknown', #Статус выполнения скрипта (failure - ошибка, success - успешное выполнение, unknown == failure)
        'memory_usage': 0, #Пик использования оперативной памяти
        'execution_time': 0, #Время выполнения
        'cpu_usage': 0, #Процент от общей мощности процессора, используемой в момент выполнения основного скрипта
        'availability': 'down' #Доступность API сервера
    }

    tracemalloc.start()

    try:
        start_func()
        metrics['exec_status'] = 'success'
    except Exception as e:
        metrics['exec_status'] = 'failure'
        log.error(f'Скрипт {script_name} завершился с ошибкой! Ошибка: {str(e)}\n{traceback.format_exc()}')
    finally:
        current_memory_usage, max_memory_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        end_time = time.time()

        metrics['memory_usage'] = max_memory_usage / (1024 * 1024)  # Convert to MB
        metrics['execution_time'] = int((end_time - start_time) * 1000)  # Convert to milliseconds
        metrics['cpu_usage'] = process.cpu_percent()
        metrics['availability'] = 'up' if metrics['exec_status'] == 'success' else 'down'

        log.info(f'{script_name} = {metrics}')

        response = requests.post('http://127.0.0.1:5000/data', json=metrics)

    print(metrics)