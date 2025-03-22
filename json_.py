import json

# Пример 1: Простой словарь
data1 = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

json_string1 = json.dumps(data1)
print("Пример 1:")
print(json_string1)
print(type(json_string1))  # Проверяем, что это строка

# Пример 2: Список словарей
data2 = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 40}
]

json_string2 = json.dumps(data2)
print("\nПример 2:")
print(json_string2)

# Пример 3: Использование indent для форматирования
data3 = {
    "name": "Charlie",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zip": "12345"
    },
    "skills": ["Python", "JavaScript", "SQL"]
}

json_string3 = json.dumps(data3, indent=4)  # Отступ в 4 пробела
print("\nПример 3 (с отступом):")
print(json_string3)

# Пример 4: Использование separators для компактности
data4 = {
    "name": "David",
    "age": 35,
    "city": "Los Angeles"
}

json_string4 = json.dumps(data4, separators=(',', ':')) # Убираем пробелы после запятых и двоеточий
print("\nПример 4 (компактный):")
print(json_string4)

# Пример 5: Сортировка ключей
data5 = {
    "b": 2,
    "a": 1,
    "c": 3
}

json_string5 = json.dumps(data5, sort_keys=True) # Сортировка ключей по алфавиту
print("\nПример 5 (сортировка ключей):")
print(json_string5)

# Пример 6: Преобразование объекта Python в JSON (не напрямую, нужно предварительное преобразование)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return self.__dict__  # Преобразуем атрибуты объекта в словарь

person = Person("Eve", 28)

# Важно: Просто так json.dumps() не сможет преобразовать объект.
# Нужно либо реализовать метод to_dict() или использовать кастомный Encoder.

json_string6 = json.dumps(person.to_dict())
print("\nПример 6 (объект Python):")
print(json_string6)

# Пример 7: Работа с Unicode
data7 = {
    "name": "Иван",  # Имя на русском языке
    "city": "Москва"
}

json_string7 = json.dumps(data7, ensure_ascii=False) # Разрешаем использование не-ASCII символов
print("\nПример 7 (Unicode):")
print(json_string7)