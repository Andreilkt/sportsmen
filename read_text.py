import json

def process_and_combine_data(json_file, text_files, json_key_to_match, text_field_for_filename, output_file):
    """
    Считывает данные из JSON файла, фильтрует их, затем считывает данные из трех
    текстовых файлов, фильтрует и объединяет все в один JSON файл, имя которого
    основано на значении поля из одного из текстовых файлов.  Версия без модуля os.

    Args:
        json_file (str): Путь к входному JSON файлу.
        text_files (list): Список путей к трем текстовым файлам.
        json_key_to_match (str): Ключ в JSON, по которому нужно фильтровать.
        text_field_for_filename (str): Поле в текстовых файлах, которое будет использоваться для имени выходного файла.
        output_file (str): Полный путь к выходному JSON файлу (включая имя файла).
    """

    # 1. Считываем и фильтруем данные из JSON файла
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: JSON файл '{json_file}' не найден.")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: JSON файл '{json_file}' содержит некорректный JSON.")
        return

    if not isinstance(json_data, list):  # Предполагаем, что в JSON файле список объектов
        print("Ошибка: JSON файл должен содержать список объектов.")
        return

    # Пример фильтрации (замените логику на вашу)
    # В данном случае, мы выбираем объекты, где поле 'status' равно 'active'
    filtered_json_data = [item for item in json_data if item.get(json_key_to_match) == 'active']

    # 2. Считываем и обрабатываем данные из текстовых файлов
    combined_text_data = []
    filename_value = None  # Для хранения значения поля для имени файла

    for text_file in text_files:
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                # file_name = text_file.split('/')[-1]  # извлекаем имя файла из пути
                for line in f:
                    # Предполагаем, что каждая строка в текстовом файле - это объект
                    # с полями, разделенными запятыми (CSV).  Замените логику разбора на вашу.
                    fields = line.strip().split(',')
                    if len(fields) >= 3:  # Пример: id,name,value
                        data = {
                            "id": fields[0],
                            "name": fields[1],
                            "value": fields[2],

                            "source": text_file # Используем переданное имя файла
                        }
                        combined_text_data.append(data)

                        # Получаем значение для имени файла (только из первого текстового файла)
                        if filename_value is None and text_field_for_filename in data:
                            filename_value = data[text_field_for_filename]
        except FileNotFoundError:
            print(f"Ошибка: Текстовый файл '{text_file}' не найден.")
            continue  # Переходим к следующему файлу
        except Exception as e:
            print(f"Ошибка при чтении текстового файла '{text_file}': {e}")
            continue

    # 3. Объединяем данные
    final_data = {
        "json_data": filtered_json_data,
        "text_data": combined_text_data
    }

    # # 4. Определяем имя выходного файла - Убрано, имя файла передается напрямую

    # 5. Записываем данные в JSON файл
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        print(f"Данные успешно записаны в файл '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи в файл '{output_file}': {e}")


# Пример использования
json_file = 'data.json' # Замените на ваш JSON файл
text_files = ['text_files/file1.txt', 'text_files/file2.txt', 'text_files/file3.txt']  # Замените на список путей к текстовым файлам
json_key_to_match = 'status'
text_field_for_filename = 'id'  # Поле, которое будет использоваться для имени файла
output_file = 'output/combined_data.json'  # Полный путь к выходному файлу (включая имя)

process_and_combine_data(json_file, text_files, json_key_to_match, text_field_for_filename, output_file)