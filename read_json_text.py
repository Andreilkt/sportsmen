
import json
from datetime import datetime, timedelta


# Функция для вычисления разницы во времени
def calculate_time_difference(end_time_str, start_time_str):
    # Преобразуем строки формата ЧЧ:ММ:СС в объекты datetime
    end_time = datetime.strptime(end_time_str, "%H:%M:%S")
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    # Разница во времени
    difference = end_time - start_time

    # Если разница отрицательная, добавляем 24 часа
    if difference < timedelta(0):
        difference += timedelta(days=1)

        # Преобразуем разницу в нужный формат ЧЧ:ММ:СС
    total_seconds = int(difference.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def process_json(input_file, output_dir, key_to_match, categories_to_process, keys_to_extract):
    """
    Читает JSON из файла, фильтрует его по нескольким категориям и записывает в разные файлы.

    Args:
        input_file (str): Путь к входному JSON файлу.
        output_dir (str): Путь к каталогу для выходных файлов (используется только для формирования имени файла).
        key_to_match (str): Ключ для фильтрации.
        categories_to_process (list): Список категорий для обработки.
        keys_to_extract (list): Список ключей для извлечения.
    """

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{input_file}' содержит некорректный JSON.")
        return

    if not isinstance(data, list):
        print("Ошибка: Входной JSON файл должен содержать список.")
        return

    # ВНИМАНИЕ: Без os или pathlib мы НЕ МОЖЕМ СОЗДАТЬ ДИРЕКТОРИЮ!
    # Убедитесь, что директория 'output_dir' существует заранее!
    # В противном случае запись в файл вызовет ошибку.


    for category in categories_to_process:
        output_file = output_dir + "/" + f"{category}.json"  # Формируем имя файла строкой
        filtered_data = []
        for item in data:
            try:
                time_difference = calculate_time_difference(item['Время финиша'], item['Время старта'])
                item['Времяфиниша'] = item.pop('Время финиша')
                item['Времястарта'] = item.pop('Время старта')
                item['Время'] = time_difference
            except KeyError:
                print(f"Предупреждение: Отсутствуют ключи 'Время финиша' или 'Время старта' для элемента. Устанавливаем время в None.")
                item['Время'] = None

            item['Имя и Фамилия'] = f"{item.get('Имя', '')} {item.get('Фамилия', '')}"
            item.pop('Имя', None)
            item.pop('Фамилия', None)

            if isinstance(item, dict) and key_to_match in item and item[key_to_match] == category:
                extracted_item = {key: item.get(key) for key in keys_to_extract}
                filtered_data.append(extracted_item)

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, indent=4, ensure_ascii=False)
            print(f"Данные успешно записаны в файл '{output_file}'.")
        except Exception as e:
            print(f"Ошибка при записи в файл '{output_file}': {e}")


def combine_data(output_dir, prize_files, categories_to_process, place=None):
    """
    Читает текстовые файлы и объединяет с JSON, созданным process_json.

    Args:
        output_dir (str): Директория, где лежат отфильтрованные json.
        prize_files (list): Список путей к файлам с призами.
        categories_to_process (list): Список категорий.
    """


    prizes = []
    for prize_file in prize_files:
        try:
            with open(prize_file, 'r', encoding='utf-8') as f:
                prizes_temp = []
                for line in f:
                    prizes_temp.append(line.strip()) # упрощенное чтение призов
                prizes.extend(prizes_temp)

        except FileNotFoundError:
            print(f"Ошибка: Файл '{prize_file}' не найден.")
            return

    for category in categories_to_process:
        json_file = output_dir + "/" + f"{category}.json" # формируем путь строкой

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{json_file}' не найден.")
            return
        except json.JSONDecodeError:
            print(f"Ошибка: Файл '{json_file}' содержит некорректный JSON.")
            return


        combined_data = {
            "Категория": category,
            "results": json_data,
            "prizes": prizes,
            "место" : place,
        }

        combined_output_file = output_dir + "/" + f"{category}_combined.json"  # формируем путь строкой
        try:
            with open(combined_output_file, 'w', encoding='utf-8') as outfile:
                json.dump(combined_data, outfile, indent=4, ensure_ascii=False)

            print(f"Объединенные данные записаны в '{combined_output_file}'.")

        except Exception as e:
            print(f"Ошибка записи в файл '{combined_output_file}': {e}")



# 1. Параметры и вызовы функций:
input_file = 'data/race_data.json'
output_directory = 'output'
key_to_match = 'Категория'
categories = ['M15', 'M16', 'M18', 'w15', 'w16','w17']
keys_to_extract = ['Нагрудный номер', 'Имя и Фамилия', 'Время', 'Категория']

prize_files = ['data/prizes_list_m15.txt', 'data/prizes_list_m16.txt', 'data/prizes_list_m18.txt']

# Перед запуском убедитесь, что директория 'output' существует!

# Вызываем функцию для фильтрации и создания файлов
process_json(input_file, output_directory, key_to_match, categories, keys_to_extract)

# Вызываем функцию для объединения и записи данных
combine_data(output_directory, prize_files, categories)