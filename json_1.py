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


def process_json(input_file, output_file, key_to_match, value_to_match, keys_to_extract):
    """
    Читает JSON из файла, преобразует в список словарей, фильтрует элементы
    по заданному ключу и значению, извлекает определенные ключи из отфильтрованных
    элементов и записывает результат в другой JSON файл.

    Args:
        input_file (str): Путь к входному JSON файлу.
        output_file (str): Путь к выходному JSON файлу.
        key_to_match (str): Ключ, по которому нужно фильтровать элементы.
        value_to_match (any): Значение, которое должно соответствовать ключу для фильтрации.
        keys_to_extract (list): Список ключей, которые нужно извлечь из отфильтрованных элементов.
    """

    try:
        with open(input_file, 'r') as f:
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

    # Фильтрация и извлечение данных
    filtered_data = []
    for item in data:
        # Вычисляем разницу во времени
        time_difference = calculate_time_difference(item['Время финиша'], item['Время старта'])

        # Создаем новые поля без пробелов
        item['Времяфиниша'] = item.pop('Время финиша')
        item['Времястарта'] = item.pop('Время старта')
        item['Время'] = time_difference  # Сохраняем разницу в минутах

        item['Имя и Фамилия'] = f"{item['Имя']} {item['Фамилия']}"
        # Удаляем старые поля, если они больше не нужны
        del item['Имя']
        del item['Фамилия']

        if isinstance(item, dict) and key_to_match in item and item[key_to_match] == value_to_match:
            extracted_item = {key: item.get(key) for key in keys_to_extract}  # .get() чтобы избежать KeyError
            filtered_data.append(extracted_item)

    # Запись в выходной файл
    try:
        with open(output_file, 'w') as f:
            json.dump(filtered_data, f, indent=4, ensure_ascii=False)
        print(f"Данные успешно записаны в файл '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи в файл '{output_file}': {e}")
        return


# 2. Вызываем функцию:
input_file = 'data/race_data.json'
output_file = 'output.json'
key_to_match = 'Категория'
value_to_match = "M15"
keys_to_extract = ['Нагрудный номер', 'Имя и Фамилия', 'Время', 'Категория']

process_json(input_file, output_file, key_to_match, value_to_match, keys_to_extract)


# Функция для считывания данных из JSON файла
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)


# Функция для считывания данных из текстового файла
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        return infile.read().strip()  # Удаляем лишние пробелы и символы новой строки


# Считываем данные из JSON файла
json_data = read_json_file('output.json')

# Выбираем нужное поле (например, 'name' из первого объекта)
chosen_name = json_data[0]['Категория']  # Здесь можно изменить индекс для выбора другого объекта

# Создаем словарь для записи данных
combined_data = {
    "Категория": chosen_name,
    "additional_info": []
}

# Считываем строки из текстовых файлов и добавляем их в 'additional_info'
for file in ['data/prizes_list_m15.txt', 'data/prizes_list_m16.txt', 'data/prizes_list_m18.txt']:
    info = read_text_file(file)
    combined_data['additional_info'].append(info)

# Название выходного файла основано на выбранном поле
output_filename = f"{chosen_name}.json"

# Записываем все данные в новый JSON файл
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

print(f"Данные успешно обработаны и записаны в файл: {output_filename}")
