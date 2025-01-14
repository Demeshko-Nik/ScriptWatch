import time
import psutil
from script_watch import monitor_script

memory_usage = 0
def example_script():
    data = []
    i=0
    process = psutil.Process()

    try:
        while True:
            i+=1
            # Добавляем элементы в список, чтобы увеличить потребление памяти
            data.append(" " * 10 ** 6)  # Добавляем строку из 1 миллиона символов
            memory_usage = process.memory_info().rss / (1024 * 1024)  # В мегабайтах
            print(f"Использовано памяти: {memory_usage:.2f} MB")
            time.sleep(0.1)  # Задержка для удобства наблюдения
            if i == 50:
                break
    except MemoryError:
        print("Оперативная память заполнена!")
    raise Exception("Something went wrong")

if __name__ == "__main__":
    monitor_script('example_script', example_script)




