
# функция считывания файла в список и дальнейшее  различное использование
def read2list(file):
    # открываем файл в режиме чтения
    file = open(file, 'r', encoding='utf-8')
    # читаем все строки и удаляем переводы строк
    lines = file.readlines()
    lines1 = [line.rstrip() for line in lines]
    file.close()
    return lines1


# вызов функции
lines = read2list('data/prizes_list_m15.txt')

# print(lines)
# поиск строки по
# префиксу, и запись в файл
pr = ('1', '2', '3')
pr_end = ('ль')
# Переменная для выбора символа в начале строки


with open('wr1.txt', 'w', encoding='utf-8') as file_for_json:
    for listitem in lines:
        if listitem.startswith(pr) and listitem.endswith(pr_end):
            file_for_json.writelines(listitem.rstrip('\n') + '\\n \n')

lines_n = read2list('wr1.txt')

# lines_n[3] = 'name'
print(lines_n)


